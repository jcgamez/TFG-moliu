using System.Collections;
using System.Collections.Generic;
using TMPro;
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.Networking;

namespace MoliuGame
{
    public class ActivitiesMenuManager : MonoBehaviour
    {
        public TextMeshProUGUI LoadingText;
        public GameObject ActivityButtonPrefab;

        private ActivityList _activities;

        void Start()
        {
            StartCoroutine(GetDataCoroutine());
        }

        IEnumerator GetDataCoroutine()
        {
            LoadingText.text = "Cargando...";
            string uri = Settings.MoliuServerURL + "/api/activities";

            using (UnityWebRequest request = UnityWebRequest.Get(uri))
            {
                yield return request.SendWebRequest();

                if (request.result == UnityWebRequest.Result.ConnectionError)
                    LoadingText.text = "Error al conectar al servidor de Moliu";
                else
                {
                    _activities = ActivityList.CreateFromJSON(request.downloadHandler.text);
                    LoadingText.enabled = false;
                    DrawActivities();
                }
            }
        }

        public void DrawActivities()
        {
            foreach (var activity in _activities.activities)
            {
                GameObject obj = Instantiate(ActivityButtonPrefab);
                GameObject panel = GameObject.Find("Panel");

                obj.transform.SetParent(panel.transform, false);
                obj.transform.GetChild(0).GetComponent<TextMeshProUGUI>().text = activity.name;
                obj.transform.GetChild(1).GetComponent<TextMeshProUGUI>().text = "Puntos: " + activity.points.Count;

                obj.GetComponent<Button>().onClick.AddListener(() => SelectActivity(activity));
            }
        }

        public void SelectActivity(Activity activity)
        {
            GameManager.Activity = activity;
            MenusManager.ChangeToScene("Game");
        }
    }
}
