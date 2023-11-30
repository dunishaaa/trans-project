using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;

public class Model: MonoBehaviour
{
    public int numberCars = 1, numberPedestrians = 1;
    public float speed, rotationSpeed, pedestrianSpeedFactor = 4f;
    public float errTolerance = 1f;

    public List<GameObject> carsList;
    public List<GameObject> metrobusList;
    public List<GameObject> pedestriansList;



    private Dictionary<int, GameObject> cars;
    private Dictionary<int, GameObject> metrobuses;
    private Dictionary<int, GameObject> pedestrians;
    private float factor = 10f;
    private float pedestrianY = 8f, floorY = 2f;
    private float xd, yd, zd;
    private void Awake()
    {
        cars = new Dictionary<int, GameObject>();
        metrobuses = new Dictionary<int, GameObject>();
        pedestrians = new Dictionary<int, GameObject>();
    }

    private void Start()
    {
        InitializeModel();
    }


    private void Update()
    {
        float totalDistance = 0f;
        foreach (var kvp in cars)
        {
            GameObject val = kvp.Value;
            Transform transform = val.GetComponent<Transform>();
            Car car = val.GetComponent<Car>();
            totalDistance += Vector3.Distance(car.targetPosition, transform.position);

        }

        foreach(var kvp in metrobuses){
            GameObject val = kvp.Value;
            Transform transform = val.GetComponent<Transform>();
            Metrobus metrobus = val.GetComponent<Metrobus>();
            totalDistance += Vector3.Distance(metrobus.targetPosition, transform.position);
        }

        foreach(var kvp in pedestrians){
            GameObject val = kvp.Value;
            Transform transform = val.GetComponent<Transform>();
            Pedestrian pedestrian = val.GetComponent<Pedestrian>();
            totalDistance += Vector3.Distance(pedestrian.targetPosition, transform.position);
        }



        totalDistance /= cars.Count + metrobuses.Count + pedestrians.Count;

        if(totalDistance < errTolerance)
        {
            StartCoroutine(GetData((modelData) =>
            {
                UpdateAgents(modelData);
            }));
        }

    }


    private (float, float) TransformCoordinates((float, float ) position)
    {
        position.Item1 *= factor;
        position.Item2 *= factor;
        return position;

    }

    private IEnumerator GetDataInit(Action<ModelData> callback)
    {
        string url = "http://127.0.0.1:5000/init/" + numberCars + "/" + numberPedestrians;
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

        string url = "http://127.0.0.1:5000/data/" + 0;

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
        Vector3 spawnPosition = new Vector3(position.Item1, floorY, position.Item2);
        //Vector3 spawnPosition = new Vector3(0f, 0f, 0f);
        Vector3 desiredDirection = new Vector3(xd, yd, zd);
        // 2 der || 3 izq || 0 arriba || 1 abaj
        if (agent.direction == 2) desiredDirection = new Vector3(1, 0, 0);
        else if (agent.direction == 3) desiredDirection = new Vector3(-1, 0, 0);
        else if (agent.direction == 1) desiredDirection = new Vector3(0, 0, -1);
        Quaternion looking_to = Quaternion.LookRotation(desiredDirection);


        switch (agentType)
        {

            case 0:
                randomIndex = UnityEngine.Random.Range(0, carsList.Count);
                GameObject newCar = carsList[randomIndex];
                newCar = Instantiate(newCar, spawnPosition, looking_to); 
                cars[agent.id] = newCar;
                break;
            case 1:
                randomIndex = UnityEngine.Random.Range(0, metrobusList.Count);
                GameObject newMetrobus= metrobusList[randomIndex];
                newMetrobus = Instantiate(newMetrobus, spawnPosition, looking_to);
                metrobuses[agent.id] = newMetrobus;
                break;
            case 2:
                randomIndex = UnityEngine.Random.Range(0, pedestriansList.Count);
                GameObject newPedestrian = pedestriansList[randomIndex];
                spawnPosition.y = pedestrianY;
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
        Vector3 nextDirection = new Vector3(position.Item1, floorY, position.Item2);
        switch (agentType)
        {
            case 0:
                currentAgent = cars[agent.id];
                Car car = currentAgent.GetComponent<Car>();
                car.speed = speed;
                car.rotationSpeed = rotationSpeed;
                car.targetPosition = nextDirection;
                break;
            case 1:
                currentAgent = metrobuses[agent.id];
                Metrobus metrobus = currentAgent.GetComponent<Metrobus>();
                metrobus.speed = speed;
                metrobus.rotationSpeed = rotationSpeed;
                metrobus.targetPosition = nextDirection;
                break;
            case 2:
                currentAgent = pedestrians[agent.id];
                Pedestrian pedestrian = currentAgent.GetComponent<Pedestrian>();
                pedestrian.speed = speed* (1f / pedestrianSpeedFactor);
                nextDirection.y = pedestrianY;
                pedestrian.targetPosition = nextDirection;
                break;

            default:
                break;
        }
    }



}
