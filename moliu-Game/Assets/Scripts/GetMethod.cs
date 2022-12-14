using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.Networking;

namespace MoliuGame
{
    public class GetMethod : MonoBehaviour
    {
        InputField outputArea;

        void Start()
        {
            outputArea = GameObject.Find("OutputArea").GetComponent<InputField>();
            GameObject.Find("ShowPlayersButton").GetComponent<Button>().onClick.AddListener(
                //() => StartCoroutine(GetDataCoroutine())
                //delegate() { StartCoroutine(GetDataCoroutine()); }
                //delegate () { StartCoroutine(GetDataCoroutine()); }
                GetData
            );
        }

        void GetData() => StartCoroutine(GetDataCoroutine());

        IEnumerator GetDataCoroutine()
        {
            outputArea.text = "Loading...";
            string uri = "localhost:8000/api/patients";
            using (UnityWebRequest request = UnityWebRequest.Get(uri))
            {
                yield return request.SendWebRequest();

                // if(request.isNetworkError || request.isHttpError)
                if (request.result == UnityWebRequest.Result.ConnectionError)
                    outputArea.text = request.error;
                else
                    outputArea.text = request.downloadHandler.text;
            }
        }

    }
}
