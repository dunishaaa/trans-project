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

        InitializeModel();
    }

    private void Update()
    { 
        foreach (var kvp in cars)
        {
            (int, int) key = kvp.Key;
            GameObject val = kvp.Value;
            Transform transform = val.GetComponent<Transform>();
            Car car = transform.GetComponent<Car>();
            if(Vector3.Distance(car.targetPosition, transform.position) < 1)
            {
                StartCoroutine(GetData((modelData) =>
                {
                    UpdateAgents(modelData);

                }));

            }
            break;
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
        string url = "http://127.0.0.1:5000/init";

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
            //Debug.Log(modelData.ToString());
            Debug.Log(modelData.cars);
            CreateAgents(modelData);

        }));
        /// for i in getdata() createAgent();

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
        foreach(AgentData agentData in data.cars)
        {
            CreateAgent(1, agentData);
        }

        //Pedestrian
        foreach(AgentData agentData in data.cars)
        {
            CreateAgent(2, agentData);
        }
    }



    private void CreateAgent(int agentType, AgentData agent)
    {
        // 0 car || 1 metrobus || 2 pedestrian
        float y;
        int randomIndex;
        (float, float) position = TransformCoordinates((agent.x, agent.y)); 
        
        y = 50f;
        Vector3 spawnPosition = new Vector3(position.Item1, y, position.Item2);
        switch (agentType)
        {

            case 0:
                randomIndex = UnityEngine.Random.Range(0, carsList.Count);
                GameObject newCar = carsList[randomIndex];
                newCar = Instantiate(newCar, spawnPosition, Quaternion.identity); 
                cars[agent.id] = newCar;
                break;
            case 1:
                randomIndex = UnityEngine.Random.Range(0, metrobuses.Count);
                GameObject newMetrobus= carsList[randomIndex];
                newMetrobus = Instantiate(newMetrobus, spawnPosition, Quaternion.identity);
                metrobuses[agent.id] = newMetrobus;
                break;
            case 2:
                randomIndex = UnityEngine.Random.Range(0, pedestrians.Count);
                GameObject newPedestrian = carsList[randomIndex];
                newPedestrian = Instantiate(newPedestrian, spawnPosition, Quaternion.identity);
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

        Vector3 nextDirection = new Vector3(position.Item1, 50f, position.Item2);
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
