import argparse
from make_tar_utils import tardir
import os

parser = argparse.ArgumentParser()
parser.add_argument(
    "--input",
    type=str,
    help="input folder, expecting subdirectory like train, valid or test",
)
parser.add_argument(
    "--output",
    type=str,
    help="output, generating tar files at output/dataclass/filename_{}.tar",
)
parser.add_argument(
    "--filename",
    type=str,
    default="_",
    help="the filename of the tar, generating tar files at output/dataclass/filename_{}.tar",
)
parser.add_argument("--dataclass", type=str, help="train or test or valid or all")
parser.add_argument(
    "--num_element", type=int, default=512, help="train or test or valid or all"
)
args = parser.parse_args()


def packup(args, dataclass):
    if not os.path.exists(os.path.join(args.input, dataclass)):
        print(
            "Dataclass {} does not exist, this folder does not exist. Skipping it.".format(
                dataclass
            )
        )
        return
    if os.path.exists(os.path.join(args.output, dataclass)):
        tardir(
            os.path.join(args.input, dataclass),
            os.path.join(args.output, dataclass, args.filename),
            args.num_element,
        )
    else:
        os.makedirs(os.path.join(args.output, dataclass))
        tardir(
            os.path.join(args.input, dataclass),
            os.path.join(args.output, dataclass, args.filename),
            args.num_element,
        )
    return


if __name__ == "__main__":
    if args.dataclass == "all":
        for x in ["train", "valid", "test"]:
            packup(args, x)
    elif args.dataclass in ["train", "valid", "test"]:
        packup(args, args.dataclass)
    else:
        raise Exception("Wrong dataclass, please read help.")
