using System.Collections;
using System.Collections.Generic;
using TMPro;
using UnityEngine;
using UnityEngine.SceneManagement;
using UnityEngine.Networking;
using UnityEngine.UI;

namespace MoliuGame
{
    public class GameManager : MonoBehaviour
    {
        private Game _game = new Game();
        // TODO: Add Activity as attribute and change ActivityManager to PointGenerator

        private bool _isCountdownStarted = false;
        private bool _isGameStarted = false;

        public TextMeshProUGUI CalibrationText;

        public GameObject Countdown;
        public TextMeshProUGUI CountdownText;
        public float CountdownTime = 5;
        private float CountdownTimeLeft;
        public GameObject NowText;

        public GameObject Score;
        public TextMeshProUGUI RightPointsText;
        public TextMeshProUGUI FailedPointsText;

        public GameObject TimeLeft;

        public GameObject EndGame;
        public TextMeshProUGUI GameInfoValues;

        public static Player Player;
        public static Activity Activity;

        private int _captureCount = 0;
        //private ScreenRecorder2 scrRec = new ScreenRecorder2();
        private ScreenRecorder screenRecorder;

        public GameObject Background;
        public GameObject GameMusic;
        private static List<Sprite> Shapes = new List<Sprite>();
        private static int _currentPoint = 0;

        private void Start()
        {
            GameObject.Find("MoliuThemeMusic").SetActive(false);
            screenRecorder = GameObject.Find("Main Camera").GetComponent<ScreenRecorder>();
            CountdownTimeLeft = CountdownTime;
            //scrRec.StartRecord("test.mp4", 30);
            StartCoroutine(GetShapes());
            StartCoroutine(GetBackground());
            StartCoroutine(GetMusic());
        }

        private void Update()
        {
            if (!_isGameStarted)
            {
                DoCountdown();
            }
        }

        private void DoCountdown()
        {
            if (!_isCountdownStarted && CalibrationText.text == "")
            {
                _isCountdownStarted = true;
                Countdown.SetActive(true);
            }
            else if (_isCountdownStarted && CalibrationText.text == "¡COLÓCATE DELANTE DEL KINECT PARA JUGAR!")
            {
                _isCountdownStarted = false;
                CountdownTimeLeft = CountdownTime;
                Countdown.SetActive(false);
            }
            else if (_isCountdownStarted && CountdownTimeLeft > 1)
            {
                CountdownTimeLeft -= Time.deltaTime;
                CountdownText.text = CountdownTimeLeft.ToString("f0");
            }
            else if (CountdownTimeLeft <= 1 && CountdownTimeLeft > -0.5f)
            {
                CountdownTimeLeft -= Time.deltaTime;
                Countdown.SetActive(false);
                NowText.SetActive(true);
            }
            else if (CountdownTimeLeft <= -0.5f)
            {
                _isGameStarted = true;

                NowText.SetActive(false);
                Score.SetActive(true);
                TimeLeft.SetActive(true);

                // Comment these two lines to disable screen recording during game
                screenRecorder.enabled = true;
                gameObject.GetComponent<JointsCollector>().enabled = true;

                ActivityManager am = GameObject.Find("ActivityController").GetComponent<ActivityManager>();
                StartCoroutine(am.DrawPoints());
            }
        }

        public void RaiseRightPoints()
        {
            _game.rightPoints += 1;
            RightPointsText.text = _game.rightPoints.ToString();
        }

        public void RaiseFailedPoints()
        {
            _game.failedPoints += 1;
            FailedPointsText.text = _game.failedPoints.ToString();
        }

        public void FinishGame()
        {
            Score.SetActive(false);
            TimeLeft.SetActive(false);
            screenRecorder.enabled = false;
            EndGame.SetActive(true);
            GameInfoValues.text = string.Format("{0}\n{1}\n{2}", Player.nickname, RightPointsText.text, FailedPointsText.text);
        }

        public void BackToMenu()
        {
            //scrRec.Close();
            SceneManager.LoadScene("MainMenu");
        }

        public bool IsGameStarted()
        {
            return _isGameStarted;
        }

        private IEnumerator GetShapes()
        {
            foreach (var point in Activity.points)
            {
                if(point.shape != "")
                {
                    string shapeURL = Settings.MoliuServerURL + point.shape;

                    using (UnityWebRequest uwr = UnityWebRequestTexture.GetTexture(shapeURL))
                    {
                        yield return uwr.SendWebRequest();

                        if (uwr.result != UnityWebRequest.Result.Success)
                        {
                            Debug.Log(uwr.error);
                        }
                        else
                        {
                            // Get downloaded asset texture
                            Texture2D shapeTexture = DownloadHandlerTexture.GetContent(uwr);

                            /* Create sprite from Texture2D to show it on screen
                            * https://docs.unity3d.com/ScriptReference/Sprite.Create.html
                            * 
                            * pixelsPerUnit is setted to spapeTexture.width to draw the shape image with
                            * suitable size. The bigger is the original image, the bigger is pixelsPerUnit
                            * value and the more the image is reduced.
                            * 
                            * This approach works well with square or almost-square images but
                            * not so well with rectangular images.
                            */
                            Sprite mySprite = Sprite.Create(shapeTexture,
                                                            new Rect(0.0f, 0.0f, shapeTexture.width, shapeTexture.height),
                                                            new Vector2(0.5f, 0.5f),
                                                            shapeTexture.width);
                            Shapes.Add(mySprite);
                        }
                    }
                }
            }
        }

        public static Sprite GetNextSprite()
        {
            Sprite nextSprite = Shapes[_currentPoint];
            _currentPoint++;
            return nextSprite;
        }

        private IEnumerator GetBackground()
        {
            string backgroundURL = Settings.MoliuServerURL + Activity.background;

            using (UnityWebRequest uwr = UnityWebRequestTexture.GetTexture(backgroundURL))
            {
                yield return uwr.SendWebRequest();

                if (uwr.result != UnityWebRequest.Result.Success)
                {
                    Debug.Log(uwr.error);
                }
                else
                {
                    // Get downloaded asset bundle
                    var texture = DownloadHandlerTexture.GetContent(uwr);
                    Background.GetComponent<RawImage>().texture = texture;
                }
            }
        }

        private IEnumerator GetMusic()
        {
            string musicURL = Settings.MoliuServerURL + Activity.music;

            using (UnityWebRequest www = UnityWebRequestMultimedia.GetAudioClip(musicURL, AudioType.MPEG))
            {
                yield return www.SendWebRequest();

                if (www.result == UnityWebRequest.Result.ConnectionError)
                {
                    Debug.Log(www.error);
                }
                else
                {
                    AudioClip gameMusic = DownloadHandlerAudioClip.GetContent(www);
                    GameMusic.GetComponent<AudioSource>().clip = gameMusic;
                    GameMusic.GetComponent<AudioSource>().Play();
                }
            }
        }
    }
}
