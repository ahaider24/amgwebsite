#include <stdio.h>
#include <stdlib.h>
#include <ft2build.h>
#include FT_FREETYPE_H
#include FT_OUTLINE_H
#include FT_MULTIPLE_MASTERS_H

static int first;
static int move(const FT_Vector *p, void *u) { if (!first) printf(",[\"Z\"]"); printf("%s[\"M\",%ld,%ld]",first?"":",",p->x,p->y);first=0;return 0; }
static int line(const FT_Vector *p, void *u) { printf(",[\"L\",%ld,%ld]",p->x,p->y);return 0; }
static int quad(const FT_Vector *a,const FT_Vector *b,void *u) { printf(",[\"Q\",%ld,%ld,%ld,%ld]",a->x,a->y,b->x,b->y);return 0; }
static int cubic(const FT_Vector *a,const FT_Vector *b,const FT_Vector *c,void *u) { printf(",[\"C\",%ld,%ld,%ld,%ld,%ld,%ld]",a->x,a->y,b->x,b->y,c->x,c->y);return 0; }
int main(int argc,char **argv) {
  if(argc!=3) return 1;
  FT_Library lib; FT_Face face; FT_MM_Var *mm;
  if(FT_Init_FreeType(&lib)||FT_New_Face(lib,argv[1],0,&face)) return 2;
  if(!FT_Get_MM_Var(face,&mm)) {
    FT_Fixed *coords=calloc(mm->num_axis,sizeof(FT_Fixed));
    for(unsigned i=0;i<mm->num_axis;i++) coords[i]=mm->axis[i].tag==FT_MAKE_TAG('w','g','h','t')?atol(argv[2])*65536:mm->axis[i].def;
    FT_Set_Var_Design_Coordinates(face,mm->num_axis,coords);free(coords);FT_Done_MM_Var(lib,mm);
  }
  printf("{\"family\":\"%s\",\"upem\":%d,\"glyphs\":{",face->family_name,face->units_per_EM);
  FT_Outline_Funcs funcs={move,line,quad,cubic,0,0};
  for(int c=32;c<127;c++) {
    if(FT_Load_Char(face,c,FT_LOAD_NO_SCALE|FT_LOAD_NO_HINTING)) return 3;
    printf("%s\"%d\":{\"advance\":%ld,\"commands\":[",c==32?"":",",c,face->glyph->advance.x);
    first=1;FT_Outline_Decompose(&face->glyph->outline,&funcs,NULL);
    if(!first)printf(",[\"Z\"]");printf("]}");
  }
  printf("}}\n");FT_Done_Face(face);FT_Done_FreeType(lib);return 0;
}
