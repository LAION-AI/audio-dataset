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
parser.add_argument(
    "--dataclass", type=str, default="all", help="train or test or valid or all"
)
parser.add_argument(
    "--num_element", type=int, default=512, help="train or test or valid or all"
)
parser.add_argument(
    "--start_idx", type=int, default=0, help="start index of the tar"
)
parser.add_argument(
    "--delete_file", action='store_true', help="delete the input file when making tars"
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
            start_idx=args.start_idx,
            delete_file=args.delete_file,
        )
    else:
        os.makedirs(os.path.join(args.output, dataclass))
        tardir(
            os.path.join(args.input, dataclass),
            os.path.join(args.output, dataclass, args.filename),
            args.num_element,
            start_idx=args.start_idx,
            delete_file=args.delete_file,
        )
    return


if __name__ == "__main__":
    if args.dataclass == "all":
        for x in ["train", "valid", "test"]:
            packup(args, x)
    elif args.dataclass == "none":
        os.makedirs(args.output, exist_ok=True)
        tardir(
            args.input,
            args.output,
            args.num_element,
            start_idx=args.start_idx,
            delete_file=args.delete_file,
        )
    else:  # if dataclass is in other name
        packup(args, args.dataclass)
