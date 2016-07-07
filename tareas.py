#!/usr/bin/python

import sqlite3
import argparse
import sys

# Variables globales
cur = None # Cursor

# Operaciones
def crear_tarea(descripcion):
    """ Crear una tarea con descripcion en la lista especificada,
    si no se especifica se utiliza la lista de tareas sueltas. """

    cur.execute('INSERT INTO tareas (descripcion, lista_id) VALUES (?, 1)', (descripcion,))

def eliminar_tarea(tarea_id):
    """ Eliminar una tarea """

    cur.execute('DELETE FROM tareas WHERE id=?', (tarea_id,))

def actualizar_tarea(tarea_id, descripcion):
    """ Actualizar descripcion de una tarea """

    cur.execute('UPDATE tareas SET descripcion=? WHERE id=?', (descripcion, tarea_id,))

def mostrar_tarea(tarea_id):
    """ Mostrar una tarea o todas si tarea_id = 0 """

    if tarea_id == 0:
        cur.execute('SELECT id, descripcion FROM tareas')
    else:
        cur.execute('SELECT id, descripcion FROM tareas WHERE id=?', (tarea_id,))

    tareas = cur.fetchall()
    for tarea in tareas:
        print "%s - %s" % (tarea[0], tarea[1],)

# Argumentos del programa
parser = argparse.ArgumentParser()
parser.add_argument('-a', help='Crear una tarea')
parser.add_argument('-d', type=int, help='Eliminar tarea')
parser.add_argument('-u', type=int, help='Actualizar tarea')
parser.add_argument('-p', type=int, help='Mostrar tarea')

def main():

    global cur

    con = sqlite3.connect('tareas.db')
    cur = con.cursor()

    args = parser.parse_args()

    if args.a:
        crear_tarea(args.a)
    elif args.d:
        eliminar_tarea(args.d)
    elif args.p:
        mostrar_tarea(args.p)

    con.commit()
    con.close()

if __name__ == '__main__':
    main()
