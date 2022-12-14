using System;
using System.IO;
using System.Linq;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
// KINECT CODE - Public Web Page Ref: https://rfilkov.com/2014/08/01/kinect-v2-with-ms-sdk/ 
// KINECT CODE - Public API Ref: https://ratemt.com/k2gpapi/
// KINECT CODE - Public DOC Ref: https://ratemt.com/k2docs/

namespace MoliuGame
{
    public class JointsCollector : MonoBehaviour
    {
        /* KINECT CODE BEGINNING */
        private Dictionary<KinectInterop.JointType, Vector3> _jointPositions = new Dictionary<KinectInterop.JointType, Vector3>();
        private string _jointsFilePath;
        private ActivityManager _activityManager;
        /* KINECT CODE END */
        private int _frameCount = 0;

        public char Delimiter = ';';

        void Start()
        {
            string gameDirectory = Camera.main.GetComponent<ScreenRecorder>().gameDirectory;
            _jointsFilePath = gameDirectory + "/joints.txt";
            _activityManager = GameObject.Find("ActivityController").GetComponent<ActivityManager>();

            if (!Directory.Exists(gameDirectory + "/frames/"))
            {
                Directory.CreateDirectory(gameDirectory + "/frames/");
            }

            if (!File.Exists(_jointsFilePath))
            {
                string headline = "Frame" + Delimiter;
                /* KINECT CODE BEGINNING */
                foreach (KinectInterop.JointType joint in Enum.GetValues(typeof(KinectInterop.JointType)))
                {
                    _jointPositions.Add(joint, Vector3.zero);
                    headline += joint.ToString() + "X" + Delimiter + 
                                joint.ToString() + "Y" + Delimiter + 
                                joint.ToString() + "Z" + Delimiter;
                }
                /* KINECT CODE END */

                using (StreamWriter sw = File.CreateText(_jointsFilePath))
                {
                    sw.WriteLine(headline + "PointX"+ Delimiter + "PointY");
                }
            }
            else
            {
                Debug.Log("Error: Joints file " + _jointsFilePath + " already exists!");
            }            
        }

        void Update()
        {
            /* KINECT CODE BEGINNING */
            KinectManager manager = KinectManager.Instance;
            

            if (gameObject.GetComponent<GameManager>().IsGameStarted() && manager.IsUserDetected())
            {
                UpdateJointPositions();
                WriteCoordinatesToFile();
            }
            /* KINECT CODE END */
        }

        private void UpdateJointPositions()
        {
            /*************************/
            /* KINECT CODE BEGINNING */
            /*************************/
            KinectManager manager = KinectManager.Instance;

            foreach(KinectInterop.JointType joint in _jointPositions.Keys.ToList())
            {
                Vector2 posColor = Vector2.zero;
                Vector3 posJointRaw = manager.GetJointKinectPosition(manager.GetPrimaryUserID(), (int)joint);

                if (posJointRaw != Vector3.zero)
                {
                    // 3d position to depth
                    Vector2 posDepth = manager.MapSpacePointToDepthCoords(posJointRaw);
                    ushort depthValue = manager.GetDepthForPixel((int)posDepth.x, (int)posDepth.y);

                    if (posDepth != Vector2.zero && depthValue > 0)
                    {
                        // depth pos to color pos
                        posColor = manager.MapDepthPointToColorCoords(posDepth, depthValue);

                        if (float.IsInfinity(posColor.x) && float.IsInfinity(posColor.y))
                        {
                            posColor = Vector2.zero;
                            posJointRaw.z = 0;
                        }
                    }
                }

                _jointPositions[joint] = new Vector3(posColor.x, posColor.y, posJointRaw.z);
            }
            /*******************/
            /* KINECT CODE END */
            /*******************/
        }

        private void WriteCoordinatesToFile()
        {
            if (!File.Exists(_jointsFilePath))
            {
                Debug.Log("Error: Joints file " + _jointsFilePath + " doesn't exist!");
                return;
            }

            string newLine = _frameCount.ToString() + Delimiter;
            _frameCount++;

            foreach (Vector3 jointPosition in _jointPositions.Values)
            {
                string jointX = jointPosition.x.ToString("f2");
                string jointY = jointPosition.y.ToString("f2");
                string jointZ = jointPosition.z.ToString("f2");

                newLine += jointX + Delimiter + jointY + Delimiter + jointZ + Delimiter;
            }

            newLine += _activityManager.CurrentPoint.x.ToString() + Delimiter +
                       _activityManager.CurrentPoint.y.ToString();

            using (StreamWriter sw = File.AppendText(_jointsFilePath))
            {

                sw.WriteLine(newLine);
            }
        }
    }
}
