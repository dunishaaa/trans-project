using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Solve : MonoBehaviour
{
    //Variable para modificar la velocidad del movimiento
    public float speed;
    //Variable que almacena la refencia al objeto al que se le adjunta el script (la capsula)
    private Transform m_transform;
    //Vector que guarda la posicion a la que se desea mover
    private Vector3 m_destinationPosition;
    //Lista que almacena todos lo waypoints (puntos donde se movera la capsula)
    public List<Transform> waypoints;

    //Método que se llama al iniciar el programa
    private void Start()
    {
        //Se utiliza la funcion GetComponente para obtener el transform del objeto al que se va acceder y mover
        m_transform = GetComponent<Transform>();
        //Se obtiene y guarda la posición de la capsula en la variable 
        m_destinationPosition = m_transform.position;
    }

    //´Método que se llama cada frame
    private void Update()
    {
        //Comparamos que la distacia de destino es menos de 0.5 a la posición actual del objeto
        if (Vector3.Distance(m_destinationPosition, m_transform.position) < 0.5)
        {
            //Si la posición es menor vamos a movernos al siguiente waypoint en la lista 
            //Se actualiza el punto del destino por el waypoint 0
            m_destinationPosition = waypoints[0].position;
            //Se elimina el waypoint que ya pasamos 0
            waypoints.RemoveAt(0);

            //Siempre accedemos al primero por que se van a ir recorriendo por que estamos eliminandolo despues de acceder al waypoint
        }

        //Guaradamos la posición actual del objeto y la guardamos en el vector3
        Vector3 currentPosition = m_transform.position;
        //Calculamos el vector de desplazamiennto usando la posicion destino menos la posición actual
        Vector3 displacementVector = m_destinationPosition - currentPosition;
        //Guardamos la normalizacion del vector displacement ya que solo nos interesa la dirección 
        Vector3 direction = Vector3.Normalize(displacementVector);
        //Se actualiza la nuev posicion que tendra el objeto en cada frama
        m_transform.position += direction * speed * Time.deltaTime;

    }
}
