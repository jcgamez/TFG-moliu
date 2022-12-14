using System.Collections;
using System.Collections.Generic;
using UnityEngine;
// KINECT CODE - Public Web Page Ref: https://rfilkov.com/2014/08/01/kinect-v2-with-ms-sdk/ 
// KINECT CODE - Public API Ref: https://ratemt.com/k2gpapi/
// KINECT CODE - Public DOC Ref: https://ratemt.com/k2docs/


namespace MoliuGame
{
    public class ActivityManager : MonoBehaviour
    {
        public Activity Activity;
        public GameObject PointPrefab;

        private List<Point> _allPoints = new List<Point>();
        private Vector2 _bottomLeft = Vector2.zero;
        private Vector2 _topRight = Vector2.zero;

        public int playerIndex = 0;
        /* KINECT CODE BEGINNING */
        public KinectInterop.JointType joint = KinectInterop.JointType.HandRight;
        /* KINECT CODE END */
        public Vector3 jointPosition;

        public Vector3 RightHandScreenPos = Vector3.zero;
        public Vector3 LeftHandScreenPos = Vector3.zero;

        public bool CanDrawNewPoint;
        public Point CurrentPoint;

        private void Awake()
        {
            _bottomLeft = Camera.main.ScreenToWorldPoint(new Vector3(0, 0, Camera.main.farClipPlane));
            _topRight = Camera.main.ScreenToWorldPoint(
                new Vector3(Camera.main.pixelWidth, Camera.main.pixelHeight, Camera.main.farClipPlane)
            );
        }

        // Start is called before the first frame update
        private void Start()
        {
            Activity = GameManager.Activity;
        }

        private void Update()
        {
            /*************************/
            /* KINECT CODE BEGINNING */
            /*************************/
            KinectInterop.JointType rightHandJoint = KinectInterop.JointType.HandRight;
            KinectInterop.JointType leftHandJoint = KinectInterop.JointType.HandLeft;
            KinectManager manager = KinectManager.Instance;

            if (manager && manager.IsInitialized())
            {
                if (manager.IsUserDetected(playerIndex))
                {
                    long userId = manager.GetUserIdByIndex(playerIndex);

                    if (manager.IsJointTracked(userId, (int)rightHandJoint))
                    {
                        GetHandScreenPos(manager, (int)rightHandJoint, ref RightHandScreenPos);
                        GetHandScreenPos(manager, (int)leftHandJoint, ref LeftHandScreenPos);
                    }
                }
            }
            /*******************/
            /* KINECT CODE END */
            /*******************/
        }

        public IEnumerator DrawPoints()
        {
            foreach (var point in Activity.points)
            {
                CanDrawNewPoint = false;

                Vector3 pointPosition = new Vector3(point.x, Screen.height - point.y, 0.5f);
                Camera camera = GameObject.Find("Main Camera").GetComponent<Camera>();
                Vector3 cameraRelativePosition = camera.ScreenToWorldPoint(pointPosition);

                GameObject newPointObject = Instantiate(PointPrefab, cameraRelativePosition, Quaternion.identity, transform);

                if (point.shape != "")
                {
                    newPointObject.transform.localScale = new Vector3(1, 1, 1);
                    newPointObject.GetComponent<SpriteRenderer>().sprite = GameManager.GetNextSprite();
                }
                
                PointInGame newPoint = newPointObject.GetComponent<PointInGame>();
                newPoint.ActivityManager = this;
                newPoint.TimeLeft = point.duration;
                newPoint.PosX = (int)point.x;
                newPoint.PosY = (int)point.y;

                _allPoints.Add(point);
                CurrentPoint = point;

                yield return new WaitUntil(() => CanDrawNewPoint);
            }

            yield return new WaitForSeconds(1.5f);
            //KinectManager manager = KinectManager.Instance;
            GameObject.Find("GameController").GetComponent<GameManager>().FinishGame();
        }

        /*************************/
        /* KINECT CODE BEGINNING */
        /*************************/
        // estimates screen cursor overlay position for the given hand
        private void GetHandScreenPos(KinectManager kinectManager, int iHandJointIndex, ref Vector3 handScreenPos)
        {
            long userId = kinectManager.GetUserIdByIndex(playerIndex);
            Vector3 posJointRaw = kinectManager.GetJointKinectPosition(userId, iHandJointIndex);

            if (posJointRaw != Vector3.zero)
            {
                Vector2 posDepth = kinectManager.MapSpacePointToDepthCoords(posJointRaw);
                ushort depthValue = kinectManager.GetDepthForPixel((int)posDepth.x, (int)posDepth.y);

                if (posDepth != Vector2.zero && depthValue > 0)
                {
                    // depth pos to color pos
                    Vector2 posColor = kinectManager.MapDepthPointToColorCoords(posDepth, depthValue);

                    // Scale the point to current screen
                    float scaledX = (posColor.x * Screen.width) / 1920;
                    float scaledY = (posColor.y * Screen.height) / 1080;

                    handScreenPos.x = scaledX;
                    handScreenPos.y = scaledY;

                }
            }
        }
        /*******************/
        /* KINECT CODE END */
        /*******************/
    }
}
