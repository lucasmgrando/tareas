#!/usr/bin/python

import sqlite3
import argparse
import sys

# Variables globales
cur = None
con = None

# Operaciones
def crear_tarea(args):
    """ Crear una tarea con descripcion en la lista especificada,
    si no se especifica se utiliza la lista de tareas sueltas. """

    cur.execute('INSERT INTO tareas (descripcion, lista_id) VALUES (?, 1)', (args.descripcion_tarea,))
    con.commit()
    print 'Se agrego una tarea'

def eliminar_tarea(args):
    """ Eliminar una tarea si existe """

    cur.execute('SELECT id FROM tareas WHERE id=?', (args.tarea_id,))

    if cur.fetchone() != None:

        cur.execute('DELETE FROM tareas WHERE id=?', (args.tarea_id,))
        con.commit()
        print 'Se elimino la tarea %d' % (args.tarea_id,)

    else:
        print 'No existe la tarea %d' % (args.tarea_id,)

def actualizar_tarea(args):
    """ Actualizar descripcion de una tarea si existe """

    cur.execute('SELECT id FROM tareas WHERE id=?', (args.tarea_id,))

    if cur.fetchone() != None:

        cur.execute('UPDATE tareas SET descripcion=? WHERE id=?', (args.nueva_descripcion, args.tarea_id,))
        con.commit()
        print 'Se actualizo la tarea %d' % (args.tarea_id,)

    else:
        print 'No existe la tarea %d' % (args.tarea_id,)

def mostrar_tarea(args):
    """ Mostrar una tarea o todas si tarea_id = 0 """

    if args.tarea_id == 0:
        cur.execute('SELECT id, descripcion FROM tareas')
    else:
        cur.execute('SELECT id, descripcion FROM tareas WHERE id=?', (args.tarea_id,))

    tareas = cur.fetchall()
    for tarea in tareas:
        print "%s - %s" % (tarea[0], tarea[1],)

# Argumentos del programa
parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers()

crear_parser = subparsers.add_parser('add')
crear_parser.add_argument('descripcion_tarea')
crear_parser.set_defaults(operacion=crear_tarea)

eliminar_parser = subparsers.add_parser('delete')
eliminar_parser.add_argument('tarea_id', type=int)
eliminar_parser.set_defaults(operacion=eliminar_tarea)

mostrar_parser = subparsers.add_parser('print')
mostrar_parser.add_argument('tarea_id', type=int)
mostrar_parser.set_defaults(operacion=mostrar_tarea)

actualizar_parser = subparsers.add_parser('update')
actualizar_parser.add_argument('tarea_id', type=int)
actualizar_parser.add_argument('nueva_descripcion')
actualizar_parser.set_defaults(operacion=actualizar_tarea)

def main():

    global cur, con

    con = sqlite3.connect('tareas.db')
    cur = con.cursor()

    args = parser.parse_args()

    # Ejecutar operacion
    args.operacion(args)

    con.close()

if __name__ == '__main__':
    main()
