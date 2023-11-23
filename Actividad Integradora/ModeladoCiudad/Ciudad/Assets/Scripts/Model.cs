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
//        InitializeModel();


    }

    private void Update()
    {

        // si la distancia es menor a algo, pedir el siguiente paso
    }


    private void GetData()
    {
        // llamada al servidor de todos los agentes
    }
    private void InitializeModel()
    {
        // llamar al servidor para inicializar el servidor en mesa;
        //GetData();
        /// for i in getdata() createAgent();

    }

    private void UpdateAgents()
    {

    }


    private (float, float) TransformCoordinates((float, float ) position)
    {
        return position;

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
                randomIndex = Random.Range(0, carsList.Count);
                GameObject newCar = carsList[randomIndex];
                newCar = Instantiate(newCar, spawnPosition, Quaternion.identity); 
                cars[agent.id] = newCar;
                break;
            case 1:
                randomIndex = Random.Range(0, metrobuses.Count);
                GameObject newMetrobus= carsList[randomIndex];
                newMetrobus = Instantiate(newMetrobus, spawnPosition, Quaternion.identity);
                metrobuses[agent.id] = newMetrobus;
                break;
            case 2:
                randomIndex = Random.Range(0, pedestrians.Count);
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
