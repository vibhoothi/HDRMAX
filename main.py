import argparse
import os


def main(args):
#    input = args.input
    ref = args.ref
    dist = args.dist
    fps = args.fps
    frames = args.frames
    output = args.output
#    csvpth = args.csvpth
    njobs = args.njobs
    outcsv = args.csv_out
    frame_range = args.frame_range
    # check if the path is empty
    if os.path.exists(output) and os.path.isdir(output):
        if os.listdir(output):
            raise RuntimeError(f"The feature path: {output} is not empty. Please remove all the content in the directory or choose a different directory.")

    if args.mode == 'hdrvmaf':
        commands = [
            f"python3 hdrvmaf_features.py {output} --ref {ref} --dist {dist} --fps {fps} --frames {frames} --space ycbcr --nonlinear local_m_exp  --channel 0 --vif --dlm --njobs {njobs} --frame_range {frame_range}",
            f"python3 hdrvmaf_features.py {output} --ref {ref} --dist {dist} --fps {fps} --frames {frames} --space ycbcr --nonlinear none --parameter 2 --channel 0 --vif --dlm --njobs {njobs} --frame_range {frame_range}",
            f"python3 predict.py {output} {outcsv}"
        ]
    elif args.mode == 'ssim-hdrmax':
        commands = [
            f"python3 hdrvmaf_features.py {output} --ref {ref} --dist {dist} --fps {fps} --frames {frames} --space ycbcr --nonlinear local_m_exp --channel 0 --vif --dlm --njobs {njobs} --frame_range {frame_range}",
            f"python3 extract_ssim.py {output} --ref {ref} --dist {dist} --fps {fps} --frames {frames} --space ycbcr  --channel 0 --njobs {njobs} --frame_range {frame_range}",
            f"python3 predict_hdrssim.py {output} {outcsv}",
        ]
    elif args.mode == 'msssim-hdrmax':
        commands = [
            f"python3 hdrvmaf_features.py {output} --ref {ref} --dist {dist} --fps {fps} --frames {frames} --space ycbcr --nonlinear local_m_exp --channel 0 --vif --dlm --njobs {njobs} --frame_range {frame_range}",
            f"python3 extract_msssim.py {output} --ref {ref} --dist {dist} --fps {fps} --frames {frames} --space ycbcr  --channel 0 --njobs {njobs} --frame_range {frame_range}",
            f"python3 predict_hdrmsssim.py {output} {outcsv}",
        ]
    else:
        raise ValueError(f"Unsupported mode: {args.mode}")

    for cmd in commands:
        print(cmd)
        os.system(cmd)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=['hdrvmaf', 'ssim-hdrmax', 'msssim-hdrmax'], help='Select processing mode')
    #parser.add_argument('--input', required=True, help='Input file path')
    parser.add_argument('--ref', required=True, help='Reference file path')
    parser.add_argument('--dist', required=True, help='Distorted YUV')
    parser.add_argument('--fps', required=True, help='Video FPS')
    parser.add_argument('--frames', required=True, help='Number of frames')
    parser.add_argument('--output', required=True, help='Output file path')
    #parser.add_argument('--csvpth', required=True, help='CSV path')
    parser.add_argument('--csv_out', required=True, help='CSV outputpath')
    parser.add_argument('--njobs', type=int, default=1, help='Number of jobs')
    parser.add_argument('--frame_range', required=True, help='Frame range')

    args = parser.parse_args()
    main(args)
