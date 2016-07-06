#!/usr/bin/python

import sqlite3
import argparse
import sys

# Variables globales
cur = None # Cursor

# Argumentos del programa
parser = argparse.ArgumentParser()
parser.add_argument('--crear-tarea', help='Crear una tarea', action='store_true')
parser.add_argument('--descripcion', help='Agregar o modificar la descripcion de una tarea')

# Operaciones
def crear_tarea(descripcion, lista_id=1):
    """ Crear una tarea con descripcion en la lista especificada,
    si no se especifica se utiliza la lista de tareas sueltas. """

    cur.execute('INSERT INTO tareas (descripcion, lista_id) VALUES (?, ?)', (descripcion, lista_id))

def eliminar_tarea(tarea_id):
    """ Eliminar una tarea """
    cur.execute('DELETE FROM tareas WHERE id=?', (tarea_id,))

def actualizar_tarea(tarea_id, descripcion):
    """ Actualizar descripcion de una tarea """
    cur.execute('UPDATE tareas SET descripcion=? WHERE id=?', (descripcion, tarea_id,))

def mostrar_tarea(tarea_id):
    """ Mostrar la tarea segun tarea_id """
    if tarea_id == 0:
        cur.execute('SELECT id, descripcion FROM tareas')
    else:
        cur.execute('SELECT id, descripcion FROM tareas WHERE id=?', (tarea_id,))

    tareas = cur.fetchall()
    for tarea in tareas:
        print "%s - %s" % (tarea[0], tarea[1],)

def main():

    global cur

    con = sqlite3.connect('tareas.db')
    cur = con.cursor()

    args = parser.parse_args()

    if args.crear_tarea and args.descripcion:
        crear_tarea(args.descripcion)

    con.commit()
    con.close()

if __name__ == '__main__':
    main()
