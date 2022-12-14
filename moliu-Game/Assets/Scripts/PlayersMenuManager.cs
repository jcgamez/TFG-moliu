using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using TMPro;
using UnityEngine.Networking;

namespace MoliuGame
{
    public class PlayersMenuManager : MonoBehaviour
    {
        public TextMeshProUGUI LoadingText;
        public GameObject AddPlayerButton;
        public GameObject PlayerButtonPrefab;
        public GameObject AddPlayerMenu;
        public GameObject SendPostRequestButton;

        public GameObject InputFields;
        public GameObject ErrorAddingPlayer;
        public TextMeshProUGUI ErrorMessage;

        public TMP_InputField NameInput;
        public TMP_InputField SurnameInput;
        public TMP_InputField NicknameInput;

        private PlayerList _players;

        void Start()
        {
            StartCoroutine(GetDataCoroutine());
            SendPostRequestButton.GetComponent<Button>().onClick.AddListener(() => StartCoroutine(PostPlayerCoroutine()));
        }

        IEnumerator GetDataCoroutine()
        {
            LoadingText.text = "Cargando...";
            string uri = Settings.MoliuServerURL + "/api/patients";

            using (UnityWebRequest request = UnityWebRequest.Get(uri))
            {
                yield return request.SendWebRequest();

                if (request.result == UnityWebRequest.Result.ConnectionError)
                    LoadingText.text = "Error al conectar al servidor de Moliu";
                else
                {
                    _players = PlayerList.CreateFromJSON(request.downloadHandler.text);
                    LoadingText.enabled = false;
                    AddPlayerButton.SetActive(true);
                    DrawPlayers();
                }
            }
        }

        IEnumerator PostPlayerCoroutine()
        {
            string uri = Settings.MoliuServerURL + "/api/patients";

            WWWForm form = new WWWForm();
            form.AddField("name", NameInput.text);
            form.AddField("surnames", SurnameInput.text);
            form.AddField("nickname", NicknameInput.text);

            using (UnityWebRequest request = UnityWebRequest.Post(uri, form))
            {
                yield return request.SendWebRequest();

                // if(request.isNetworkError || request.isHttpError)
                if (request.result == UnityWebRequest.Result.ConnectionError)
                {
                    InputFields.SetActive(false);
                    ErrorAddingPlayer.SetActive(true);
                    ErrorMessage.text = request.error;
                }
                else
                    MenusManager.ChangeToScene("PlayerList");
            }
        }

        public void DrawPlayers()
        {
            foreach (var player in _players.players)
            {
                GameObject obj = Instantiate(PlayerButtonPrefab);
                GameObject panel = GameObject.Find("Panel");

                obj.transform.SetParent(panel.transform, false);
                obj.transform.GetChild(0).GetComponent<TextMeshProUGUI>().text = player.nickname;
                obj.transform.GetChild(1).GetComponent<TextMeshProUGUI>().text = player.name + " " + player.surnames;
                obj.GetComponent<Button>().onClick.AddListener(() => SelectPlayer(player));
            }
        }

        public void SelectPlayer(Player player)
        {
            GameManager.Player = player;
            MenusManager.ChangeToScene("ActivityList");
            //SceneManager.LoadScene("ActivityList");
        }

        public void showAddPlayerMenu(bool isActive)
        {
            AddPlayerMenu.SetActive(isActive);
            InputFields.SetActive(true);
            ErrorAddingPlayer.SetActive(false);
            NameInput.text = "";
            SurnameInput.text = "";
            NicknameInput.text = "";
        }
    }
}
