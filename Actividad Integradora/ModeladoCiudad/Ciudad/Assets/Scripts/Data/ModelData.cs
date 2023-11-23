using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System;

[Serializable]
public class ModelData
{
    (int, int) gridSize;
    List<AgentData> cars;
    List<AgentData> metrobuses;
    List<AgentData> pedestrians;
}
