python simple_stackplots.py --mode=SL --sel=presel_2b
python simple_stackplots.py --mode=DL --sel=presel_2b

python print_cutflow_table.py  --notopw --notrig > tables/cat_table_WP80_trigger_notopw.tex
python print_cutflow_table.py  --notopw > tables/cat_table_WP80_trigger_notopw.tex
python print_cutflow_table.py>tables/cut_table_WP80_trigger.tex

python print_cutflow_table_by_category.py --mode=SL --notopw > tables/comp_table_WP80_trigger_notopw.tex
python print_cutfolw_table_by_category.py --mode=SL> tables/comp_table_WP80_trigger_notopw.tex
