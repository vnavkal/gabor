import os
import argparse
import gabor
import video_processing


ACTIVATION_FRAME_DIRECTORY = 'filtered_frames'

if __name__ == '__main__':
    argparser = argparse.ArgumentParser(
        description='Download YouTube driving video and attempt lane detection'
    )
    argparser.add_argument(
        '--frequency',
        dest='frequency',
        help='frequency at which video frames are sampled',
        type=float,
        default=20.
    )
    argparser.add_argument(
        '--num-frames',
        dest='num_frames',
        help='number of frames to process',
        type=int,
        default=40
    )
    argparser.add_argument(
        '--video-path',
        dest='video_path',
        help='path of input video',
        required=True
    )
    argparser.add_argument(
        '--num-processes',
        dest='num_processes',
        help='number of processes to use for calculating convolutions',
        type=int,
        default=12
    )
    argparser.add_argument(
        '--rescaling-factor',
        dest='rescaling_factor',
        help='factor by which to rescale video (choosing a value less than 1 can speed processing)',
        type=float,
        default=.4
    )

    args = argparser.parse_args()

    if not os.path.exists(args.video_path):
        print('Downloading video')
        video_processing.download_video(args.video_path)


    print('Splitting video into frames')
    video_processing.capture_frames(args.video_path,
                                    frequency=args.frequency,
                                    num_frames=args.num_frames)

    f = gabor.get_best_filter(args.rescaling_factor)
    grayscales = [gabor.load_frame(i, args.rescaling_factor) for i in range(args.num_frames)]

    print('Convolving (this may take a while)')
    convolved_grayscales = gabor.apply_filter(f, grayscales, args.num_processes)

    activations = [gabor.get_activations(x, .9998) for x in convolved_grayscales]

    gabor.save_activations(activations, ACTIVATION_FRAME_DIRECTORY)

    video_processing.assemble_frames('filtered_lanes.mp4',
                                     input_directory=ACTIVATION_FRAME_DIRECTORY,
                                     frequency=args.frequency)
