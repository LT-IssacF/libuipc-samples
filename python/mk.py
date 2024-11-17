import shutil as sh
import argparse as ap
import pathlib as pl


def main():
    parser = ap.ArgumentParser(description='Create libuipc sample')
    parser.add_argument('name', type=str, help='Name of the sample')
    args = parser.parse_args()
    
    this_file = pl.Path(__file__).resolve()
    this_folder = this_file.parent
    temp_sim_0 = pl.Path(this_folder / 'templates' / 'sim_0').resolve()
    
    # find all folders in this folder
    folders = [f for f in this_folder.iterdir() if f.is_dir()]
    # find out the folders start with number
    f_map = {}
    for f in folders:
        number = f.name.split('_')[0]
        if number.isdigit():
            f_map[int(number)] = f
    
    # find the max number
    max_number = max(f_map.keys())
    # create the new folder
    new_folder = this_folder / f'{max_number+1}_{args.name}'
    sh.copytree(temp_sim_0, new_folder)

if __name__ == '__main__':
    main()