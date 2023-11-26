using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;

public class Model: MonoBehaviour
{
    public float factor = 10f;
    public List<GameObject> carsList;
    public List<GameObject> metrobusList;
    public List<GameObject> pedestriansList;

    public int number_cars = 1;
    public float err_tolerance = 1f;
    public float floor_y = -14.1f;


    public List<GameObject> agents;
    public Dictionary<int, GameObject> cars;
    public Dictionary<int, GameObject> metrobuses;
    public Dictionary<int, GameObject> pedestrians;


    private void Start()
    {
        cars = new Dictionary<int, GameObject>();
        metrobuses = new Dictionary<int, GameObject>();
        pedestrians = new Dictionary<int, GameObject>();
        InitializeModel();

    }

    private void Update()
    {
        float totalDistance = 0f;
        foreach (var kvp in cars)
        {
            int key = kvp.Key;
            GameObject val = kvp.Value;
            Transform transform = val.GetComponent<Transform>();
            Car car = transform.GetComponent<Car>();
            totalDistance += Vector3.Distance(car.targetPosition, transform.position);

        }

        totalDistance /= (float)cars.Count;

        if(totalDistance < err_tolerance)
        {
            StartCoroutine(GetData((modelData) =>
            {
                UpdateAgents(modelData);
            }));
        }



        
        // si la distancia es menor a algo, pedir el siguiente paso
    }

    private (float, float) TransformCoordinates((float, float ) position)
    {
        position.Item1 *= factor;
        position.Item2 *= factor;
        return position;

    }

    private IEnumerator GetDataInit(Action<ModelData> callback)
    {
        string url = "http://127.0.0.1:5000/init/" + number_cars;
        using (UnityWebRequest getRequest = UnityWebRequest.Get(url))
        {
            yield return getRequest.SendWebRequest();

            if (getRequest.result == UnityWebRequest.Result.Success) {
                string response = getRequest.downloadHandler.text;
                Debug.Log(response);
                ModelData modelData = JsonUtility.FromJson<ModelData>(response);
                callback?.Invoke(modelData);
            }
            else
            {
                Debug.Log("Server connection failed!");
            }

        }

        // llamada al servidor de todos los agentes
    }
    private IEnumerator GetData(Action<ModelData> callback)
    {

        string url = "http://127.0.0.1:5000/data";

        using (UnityWebRequest getRequest = UnityWebRequest.Get(url))
        {
            yield return getRequest.SendWebRequest();

            if (getRequest.result == UnityWebRequest.Result.Success) {
                string response = getRequest.downloadHandler.text;
                Debug.Log(response);
                ModelData modelData = JsonUtility.FromJson<ModelData>(response);
                callback?.Invoke(modelData);
            }
            else
            {
                Debug.Log("Server connection failed!");
            }

        }

        // llamada al servidor de todos los agentes
    }
    private void InitializeModel()
    {
        StartCoroutine(GetDataInit((modelData) =>
        {
            CreateAgents(modelData);
            Debug.Log("number of cars: " + cars.Count);

        }));

    }

    private void UpdateAgents(ModelData data)
    {
        //Cars
        foreach(AgentData agentData in data.cars)
        {
            UpdateAgent(0, agentData);
        }
        //Metrobus
        foreach(AgentData agentData in data.metrobuses)
        {
            UpdateAgent(1, agentData);
        }

        //Pedestrian
        foreach(AgentData agentData in data.pedestrians)
        {
            UpdateAgent(2, agentData);
        }
    }
    private void CreateAgents(ModelData data)
    {
        //Cars
        foreach(AgentData agentData in data.cars)
        {
            CreateAgent(0, agentData);
        }
        //Metrobus
        foreach(AgentData agentData in data.metrobuses)
        {
            CreateAgent(1, agentData);
        }

        //Pedestrian
        foreach(AgentData agentData in data.pedestrians)
        {
            CreateAgent(2, agentData);
        }
    }



    private void CreateAgent(int agentType, AgentData agent)
    {
        // 0 car || 1 metrobus || 2 pedestrian
        int randomIndex;
        (float, float) position = TransformCoordinates((agent.x, agent.y)); 

        
        Debug.Log("Agent id on creation: " + agent.id);
        Vector3 spawnPosition = new Vector3(position.Item1, floor_y, position.Item2);
        Quaternion looking_to = Quaternion.Euler(0f, 0f, 0f);
        switch (agentType)
        {

            case 0:
                randomIndex = UnityEngine.Random.Range(0, carsList.Count);
                GameObject newCar = carsList[randomIndex];
                newCar = Instantiate(newCar, spawnPosition, looking_to); 
                cars[agent.id] = newCar;
                break;
            case 1:
                randomIndex = UnityEngine.Random.Range(0, metrobuses.Count);
                GameObject newMetrobus= carsList[randomIndex];
                newMetrobus = Instantiate(newMetrobus, spawnPosition, looking_to);
                metrobuses[agent.id] = newMetrobus;
                break;
            case 2:
                randomIndex = UnityEngine.Random.Range(0, pedestrians.Count);
                GameObject newPedestrian = carsList[randomIndex];
                newPedestrian = Instantiate(newPedestrian, spawnPosition, looking_to);
                pedestrians[agent.id] = newPedestrian;
                break;
            default:
                break;
        }
    }

   
    private void UpdateAgent(int agentType, AgentData agent)
    {
        GameObject currentAgent;
        (float, float) position = TransformCoordinates((agent.x, agent.y));


        Debug.Log("Updating car with id: " + agent.id);
        Vector3 nextDirection = new Vector3(position.Item1, floor_y, position.Item2);
        switch (agentType)
        {
            case 0:
                currentAgent = cars[agent.id];
                Car car = currentAgent.GetComponent<Car>();
                car.targetPosition = nextDirection;
                break;
            case 1:
                currentAgent = metrobuses[agent.id];
                Metrobus metrobus = currentAgent.GetComponent<Metrobus>();
                metrobus.targetPosition = nextDirection;
                break;
            case 2:
                currentAgent = pedestrians[agent.id];
                Pedestrian pedestrian = currentAgent.GetComponent<Pedestrian>();
                pedestrian.targetPosition = nextDirection;
                break;
            default:
                break;
        }
    }



}
