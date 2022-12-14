using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.Networking;
using UnityEngine.SceneManagement;

namespace MoliuGame
{
    public class GetActivities : MonoBehaviour
    {
        InputField outputArea;
        public static Activity ActivitySelected;

        void Start()
        {
            outputArea = GameObject.Find("OutputArea").GetComponent<InputField>();
            //StartCoroutine(GetDataCoroutine());
            GameObject.Find("ShowActivitiesButton").GetComponent<Button>().onClick.AddListener(
               () => StartCoroutine(GetDataCoroutine())
           );
        }

        IEnumerator GetDataCoroutine()
        {
            outputArea.text = "Cargando...";
            string uri = "localhost:8000/api/activities";

            using (UnityWebRequest request = UnityWebRequest.Get(uri))
            {
                yield return request.SendWebRequest();

                // if(request.isNetworkError || request.isHttpError)
                if (request.result == UnityWebRequest.Result.ConnectionError)
                    outputArea.text = request.error;
                else
                {
                    outputArea.text = request.downloadHandler.text;
                    ActivityList acts = ActivityList.CreateFromJSON(request.downloadHandler.text);
                    // TODO: Select activity
                    ActivitySelected = acts.activities[3];
                    SceneManager.LoadScene("Game");
                }
            }
        }

    }
}
