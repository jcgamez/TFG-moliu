using System.Collections;
using System.Collections.Generic;
using System;
using System.IO;
using UnityEngine;
using System.Drawing;
using System.Drawing.Imaging;
using FFMediaToolkit;
using FFMediaToolkit.Graphics;
using FFMediaToolkit.Encoding;

namespace MoliuGame
{
    public static class VideoCreator
    {
        //public static VideoCreator(string loaderPath)
        //{
        //    FFmpegLoader.FFmpegPath = loaderPath;
        //}
        private static bool isFFmpegPathSet = false;

        public static void setFFmpegPath(string loaderPath)
        {
            if(!isFFmpegPathSet)
            {
                FFmpegLoader.FFmpegPath = loaderPath;
                isFFmpegPathSet = true;
            }
        }

        public static void AddAllFrames(string inputDirectory, string outputFile)
        {
            // You can set there codec, bitrate, frame rate and many other options.
            var settings = new VideoEncoderSettings(width: 640, height: 360, framerate: 24, codec: VideoCodec.H264);
            settings.EncoderPreset = EncoderPreset.Fast;
            //settings.CRF = 17;

            string[] images = Directory.GetFiles(inputDirectory);

            using (var file = MediaBuilder.CreateContainer(outputFile).WithVideo(settings).Create())
            {
                for(int i=0; i<images.Length; i++)
                {
                    Bitmap bitmap = new Bitmap(images[i]);

                    var rect = new Rectangle(System.Drawing.Point.Empty, bitmap.Size);
                    var bitLock = bitmap.LockBits(rect, ImageLockMode.ReadOnly, PixelFormat.Format24bppRgb);
                    var bitmapData = ImageData.FromPointer(bitLock.Scan0, ImagePixelFormat.Bgr24, bitmap.Size);

                    file.Video.AddFrame(bitmapData); // Encode the frame

                    bitmap.UnlockBits(bitLock); // UnlockBits() must be called after encoding the frame
                }
            }
        }
    }
}
