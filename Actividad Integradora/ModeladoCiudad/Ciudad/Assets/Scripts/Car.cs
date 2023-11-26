using System.Collections;
using System.Collections.Generic;
using Unity.VisualScripting;
using UnityEditor.Rendering;
using UnityEngine;

public class Car : Vehicle 
{
    public Car()
    {
        speed = 50.0f;
        rotationSpeed = 100f;
    }  
}
