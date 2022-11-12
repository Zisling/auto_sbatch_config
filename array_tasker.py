import os

import re
import toml
import argparse
from itertools import product


def parse_args():
    parser = argparse.ArgumentParser(description='setup runs and if need start running them')
    parser.add_argument('-sr', '--start_run',
                        action='store_true', help='if used will start running the sbatch commands')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    master_conf: dict = toml.load('runs.toml')
    model_default = master_conf['default']
    sbatch_default = master_conf['sbatch']
    with open('array_run.sbatch') as f:
        sbatch_templet = ''.join(f.readlines())

    runs = {name: conf for name, conf in master_conf['runs'].items() if conf['active']}
    for name, conf in runs.items():
        common = conf['common']
        permutations_keys = conf['permute'].keys()
        product_of_permute = list(product(*conf['permute'].values()))
        if 'series' in conf:
            series_keys = conf['series'].keys()
            all_permutations = list(product(product_of_permute, list(zip(*conf['series'].values()))))
            permutations = [{**dict(zip(permutations_keys, perm)), **dict(zip(series_keys, ser)), **common}
                            for perm, ser in all_permutations]
        else:
            permutations = [{**dict(zip(permutations_keys, perm)), **common} for perm in product_of_permute]

        # set path to sbatch and configs path and create folders
        sbatch_path = os.path.join('configs', name)
        conf_path = os.path.join('configs', name, 'confs')
        os.makedirs(conf_path, exist_ok=True)

        # save the configs to run
        for i, perm in enumerate(permutations):
            run: dict = model_default.copy()
            run.update(perm)
            run['conf_num'] = i
            # write the configs to run
            with open(os.path.join(conf_path, f'{i}.toml'), 'w+') as f:
                toml.dump(run, f)

        # write the sbatch for this run
        sbatch_conf = sbatch_default.copy()
        sbatch_conf['conf_path'] = conf_path
        sbatch_conf['range'] = f'0-{len(permutations) - 1}'
        sbatch_file = sbatch_templet

        # if the config have change do them
        if 'sbatch' in conf:
            sbatch_conf.update(conf['sbatch'])
        # insert the changes
        for key, value in sbatch_conf.items():
            pattern = re.compile(re.escape(f'@{key}@'), re.IGNORECASE)
            sbatch_file = pattern.sub(value, sbatch_file)
        # write the file
        sbatch_file_path = os.path.join(sbatch_path, f'{name}.sbatch')
        with open(sbatch_file_path, 'w+') as f:
            f.write(sbatch_file)

        if args.start_run:
            os.system(f"sbatch {sbatch_file_path}")
