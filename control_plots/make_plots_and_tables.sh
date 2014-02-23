#python simple_stackplots.py --mode=SL --sel=presel_2b --notopw
#python simple_stackplots.py --mode=DL --sel=presel_2b --notopw

python print_cutflow_table_by_category.py  --notopw --notrig > tables/cat_table_WP80_notrig_notopw.tex
python print_cutflow_table_by_category.py  --notopw > tables/cat_table_WP80_notopw.tex
#python print_cutflow_table_by_category.py > tables/cat_table_WP80.tex

python print_cutflow_table.py --notopw > tables/comp_table_WP80_notopw.tex
#python print_cutflow_table.py > tables/comp_table_WP80.tex
