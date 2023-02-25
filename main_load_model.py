import os
import sys
import yaml
import logging
import argparse
from os.path import basename, normpath, join
from datetime import datetime

from aitextgen import aitextgen

from utils.general_utils.general_utils import load_yaml
sys.path.append("./")  # needed 4 utils imports - created according to launcher


def run(path_params: str):
    # Input
    params = load_yaml(path_params)
    params_gen = params['generation']
    logging.debug(f"Params: {params}")

    model_name = "gpt2test_20230225181657"
    model_dir = join("data/models_trained", model_name)
    gpt2_model = aitextgen(model_folder=model_dir,
                           tokenizer_file="aitextgen.tokenizer.json",
                           config=join(model_dir, "config.json"),
                           to_gpu=True)

    # Generate
    prompt = gpt2_model.generate_one(prompt=params_gen['prefix'],
                                     # seed=params_gen['seed'],
                                     max_length=params_gen['max_length'],
                                     temperature=params_gen['temperature'],
                                     top_p=params_gen['top_p'],
                                     repetition_penalty=params_gen['repetition_penalty'],
                                     early_stopping=params_gen['early_stopping'],
                                     num_beams=params_gen['num_beams'])

    print(prompt)
    logging.info("Generation completed!")

    # Output persist
    model_params_path = join(model_dir, 'gpt2_scratch_params.yaml')
    with open(model_params_path, 'w') as f:
        yaml.dump(params, f, default_flow_style=False)
    logging.debug(f"Model params saved at {model_params_path}")


def main(argv):
    parser = argparse.ArgumentParser(prog=argv[0])
    parser.add_argument("--path_params", help="Path to rnn YAML params",
                        default="gpt2_scratch_params.yaml")
    parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
    args = parser.parse_args(argv[1:])
    loglevel = logging.DEBUG if args.verbose else logging.INFO
    process_name = basename(normpath(argv[0]))
    logging.basicConfig(format=f"[{process_name}][%(levelname)s]: %(message)s", level=loglevel, stream=sys.stdout)
    delattr(args, "verbose")
    run(**vars(args))


if __name__ == '__main__':
    main(sys.argv)
