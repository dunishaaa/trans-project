using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Model: MonoBehaviour
{
    public int numberOfCars = 2;
    public List<GameObject> carsList;
    public List<GameObject> metrobusList;
    public List<GameObject> pedestriansList;

    public float gridWidth;
    public float gridHeight;

    public float modelWidth;
    public float modelHeight;

    public List<GameObject> agents;
    public Dictionary<(int, int), GameObject> cars;
    public Dictionary<(int, int), GameObject> metrobuses;
    public Dictionary<(int, int), GameObject> pedestrians;


    private void Start()
    {
        cars = new Dictionary<(int, int), GameObject>();
        metrobuses = new Dictionary<(int, int), GameObject>();
        pedestrians = new Dictionary<(int, int), GameObject>();
        
        for(int i = 0; i < numberOfCars; i++)
        {
            int randomIndex = Random.Range(0, carsList.Count);
            GameObject newCar = carsList[randomIndex];

            float x, y, z;
            x = Random.Range(0, 300);
            y = 50f;
            z = Random.Range(0, 300);

            Vector3 spawnPosition = new Vector3(x, y, z);

            GameObject gb = Instantiate(newCar, spawnPosition, Quaternion.identity);

            agents.Add(gb);
        }


    }


    private void GetData()
    {

    }

    private void TransformCoordinates()
    {

    }

    private void CreateAgent(int agentType, AgentData agent)
    {
        // 0 car || 1 metrobus || 2 pedestrian
        float x, y, z;
        x = agent.x;
        y = 50f;
        z = agent.y;
        Vector3 spawnPosition = new Vector3(x, y, z);
        switch (agentType)
        {
            case 0:
                int randomIndex = Random.Range(0, carsList.Count);
                GameObject newCar = carsList[randomIndex];
                break;
            case 1:
                //imple
                break;
            case 2:
                //imple
                break;
            default:
                break;
        }
    }

    private void InitializeModel()
    {
        // llamar al servidor para inicializar el servidor en mesa;

    }

    private void UpdateAgents()
    {
    }



}
