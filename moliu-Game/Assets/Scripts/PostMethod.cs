using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.Networking;

namespace MoliuGame
{
    public class PostMethod : MonoBehaviour
    {
        InputField outputArea;

        // Start is called before the first frame update
        void Start()
        {
            outputArea = GameObject.Find("OutputArea").GetComponent<InputField>();
            GameObject.Find("AddPlayerButton").GetComponent<Button>().onClick.AddListener(PostData);
        }

        void PostData() => StartCoroutine(PostDataCoroutine());

        IEnumerator PostDataCoroutine()
        {
            outputArea.text = "Loading...";
            string uri = "localhost:8000/api/patients";

            WWWForm form = new WWWForm();
            form.AddField("name", "createdPatientFromUnity2");
            form.AddField("surnames", "surnameFromUnity");
            form.AddField("nickname", "unity2");

            using (UnityWebRequest request = UnityWebRequest.Post(uri, form))
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
