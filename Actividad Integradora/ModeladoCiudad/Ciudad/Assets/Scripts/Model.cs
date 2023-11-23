using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Model: MonoBehaviour
{
    public int numberOfCars = 2;
    public List<GameObject> carsList;
    public List<GameObject> pedestriansList;

    public float gridWidth;
    public float gridHeight;

    public float modelWidth;
    public float modelHeight;

    public List<GameObject> agents;


    private void Start()
    {
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

    private void Update()
    {
        
    }

    private void GetData()
    {

    }

    private void TransformCoordinates()
    {

    }

    private void CreateAgent()
    {
    }

    private void InitializeModel()
    {

    }

    private void UpdateAgents()
    {
    }



}
