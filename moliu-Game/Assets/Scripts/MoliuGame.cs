using System;
using System.Collections.Generic;
using UnityEngine;

namespace MoliuGame
{
    public static class Settings
    {
        public static string MoliuServerURL = "localhost:8000";
        //public static string MoliuServerURL = "eupelx13.uco.es:8100";
    }   

    [Serializable]
    public class Player
    {
        public string name;
        public string surnames;
        public string nickname;
    }

    [Serializable]
    public class PlayerList
    {
        public List<Player> players;

        public static PlayerList CreateFromJSON(string jsonString)
        {
            return JsonUtility.FromJson<PlayerList>(jsonString);
        }
    }

    [Serializable]
    public class Point
    {
        public float x;
        public float y;
        public int order;
        public string shape;
        public float duration;
    }

    [Serializable]
    public class Activity
    {
        public string name;
        public string description;
        public string background;
        public string music;
        public List<Point> points;
    }

    [Serializable]
    public class ActivityList
    {
        public List<Activity> activities;

        public static ActivityList CreateFromJSON(string jsonString)
        {
            return JsonUtility.FromJson<ActivityList>(jsonString);
        }
    }

    [Serializable]
    public class Game
    {
        public string activity;
        public string player;
        public int rightPoints;
        public int failedPoints;
    }
}
