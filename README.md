# Python Conding Dojo Katas

## K8s Read Workloads KATA

Sean los fichero estáticos .yml en static_files/OCPClusterX.yml representaciones de workloads 
de K8s

Lee los ficheros en la estructura que prefieras y hay que satisfacer los tests en read_workloads.py

Nota:

    Cada cluster puede tener un número indeterminado de nodos
    Cada nodo es único, y suma para la adición de recursos
    Un nodo puede tener o no la línea node_labels

    Los namespaces son estructuras lógicas que se replican en todos los nodos de k8s
    Su utilidad es delimitar el acceso a recursos de las aplicaciones
    En los ficheros de test cada ns tiene un nombre diferente

    Al similar ocurre con los pods, 2 pods con el mismo nombre pueden existir en ns diferentes

    Labels:

        Las etiquetas se usan para seleccionar recursos en kubernetes
        Sin embargo, son estructuras del tipo clave:valor, con sus limitaciones

        No podemos tener 2 valores diferentes para una misma clave dentro de un mismo dominio 
        de colisión

        Para ello se establece una precedencia en sentido descendente

        Consideramos "iguales" 2 claves que compartan cluster, nodo, ns o pod
        Viendo el ejemplo del cluster 1:

        Para el Pod: pod_1
        label_tier: pod1

        Para el Pod: pod_2
        label_tier: pod_2

        Las etiquetas del cluster deben contener ambos valores para esa clave
        Los tests siempre nos pedirán los valores finales, con la precedencia aplicada

        Almacenar los valores intermedios no es obligatorio



    test_get_cluster_name(input_file, expected_cluster_name)
        devuelve el cluster_name
    
    test_get_cpu_count(input_file, expected_cpu_count)
        devuelve la suma de las cpu de los nodos que forman el cluster

    test_get_mem_count(input_file, expected_mem_count)
        devuelve la suma de GB de los nodos que forman el cluster

    test_get_all_nodes()
        devuelve todos los nodos del cluster

    test_get_all_ns()
        devuelve todos los ns del cluster

    test_get_all_pods()
        devuelve todos los pods del cluster        

    test_get_ns_by_node()
        devuelve los ns de los nodos que macheen con la regex 

    test_get_pods_by_ns()
        devuelve los ns de los nodos que macheen con la regex
