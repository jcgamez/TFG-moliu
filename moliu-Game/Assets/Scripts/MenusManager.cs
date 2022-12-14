using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;

namespace MoliuGame
{
    public class MenusManager : MonoBehaviour
    {
        public static void ChangeToScene(string scene)
        {
            SceneManager.LoadScene(scene);
        }

        public void Quit()
        {
            Application.Quit();
        }
    }
}

