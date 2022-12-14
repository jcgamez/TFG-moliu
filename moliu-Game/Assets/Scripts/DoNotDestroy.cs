using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;

public class DoNotDestroy : MonoBehaviour
{
    private void Awake()
    {
        GameObject[] musicObjs = GameObject.FindGameObjectsWithTag("MoliuMusic");

        if(musicObjs.Length > 1)
            Destroy(this.gameObject);

        DontDestroyOnLoad(this.gameObject);
    }
}
