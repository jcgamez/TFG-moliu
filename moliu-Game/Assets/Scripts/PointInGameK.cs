using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using TMPro;
// KINECT CODE - Public Web Page Ref: https://rfilkov.com/2014/08/01/kinect-v2-with-ms-sdk/ 
// KINECT CODE - Public API Ref: https://ratemt.com/k2gpapi/
// KINECT CODE - Public DOC Ref: https://ratemt.com/k2docs/

namespace MoliuGame
{
    public class PointInGame : MonoBehaviour
    {
        public float TimeLeft;
        public int PosX;
        public int PosY;
        public int PixelMargin;

        public ActivityManager ActivityManager = null;
        public GameManager GameManager = null;
        /* KINECT CODE BEGINNING */
        private KinectManager manager = KinectManager.Instance;
        /* KINECT CODE END */
        private TextMeshProUGUI TimeLeftText = null;

        private SpriteRenderer _spriteRenderer = null;

        private void Awake()
        {
            _spriteRenderer = GetComponent<SpriteRenderer>();
        }

        private void Start()
        {
            ActivityManager = GameObject.Find("ActivityController").GetComponent<ActivityManager>();
            GameManager = GameObject.Find("GameController").GetComponent<GameManager>();
            TimeLeftText = GameObject.Find("TimeLeftText").GetComponent<TextMeshProUGUI>();
        }

        private void Update()
        {
            TimeLeft -= Time.deltaTime;
            TimeLeftText.text = TimeLeft.ToString("n0");

            if (TimeLeft <= 0f)
            {
                ActivityManager.CanDrawNewPoint = true;
                GameManager.RaiseFailedPoints();
                Destroy(transform.gameObject);
            }

            /*************************/
            /* KINECT CODE BEGINNING */
            /*************************/
            if (manager.IsUserDetected(0))
            {
                if(isRightHandTouchingPoint() || isLeftHandTouchingPoint())
                {
                    ActivityManager.CanDrawNewPoint = true;
                    GameManager.RaiseRightPoints();
                    Destroy(transform.gameObject);
                }
            }
        }

        private bool isRightHandTouchingPoint()
        {
            /*************************/
            /* KINECT CODE BEGINNING */
            /*************************/
            long userId = manager.GetUserIdByIndex(0);

            if (((int)ActivityManager.RightHandScreenPos.x == 0) &&
               ((int)ActivityManager.RightHandScreenPos.y == 0))
                return false;

            if (!manager.IsJointTracked(userId, (int)KinectInterop.JointType.HandRight))
                return false;

            if (((int)ActivityManager.RightHandScreenPos.x >= (PosX - PixelMargin)) && 
               ((int)ActivityManager.RightHandScreenPos.x <= (PosX + PixelMargin)) &&
               ((int)ActivityManager.RightHandScreenPos.y >= (PosY - PixelMargin)) && 
               ((int)ActivityManager.RightHandScreenPos.y <= (PosY + PixelMargin)))
                return true;
            else return false;
        }

        private bool isLeftHandTouchingPoint()
        {
            /*************************/
            /* KINECT CODE BEGINNING */
            /*************************/
            long userId = manager.GetUserIdByIndex(0);

            if (((int)ActivityManager.LeftHandScreenPos.x == 0) &&
               ((int)ActivityManager.LeftHandScreenPos.y == 0))
                return false;

            if (!manager.IsJointTracked(userId, (int)KinectInterop.JointType.HandLeft))
                return false;

            if (((int)ActivityManager.LeftHandScreenPos.x >= (PosX - PixelMargin)) && 
               ((int)ActivityManager.LeftHandScreenPos.x <= (PosX + PixelMargin)) &&
               ((int)ActivityManager.LeftHandScreenPos.y >= (PosY - PixelMargin)) && 
               ((int)ActivityManager.LeftHandScreenPos.y <= (PosY + PixelMargin)))
                return true;
            else return false;
            /*******************/
            /* KINECT CODE END */
            /*******************/
        }
    }
}
