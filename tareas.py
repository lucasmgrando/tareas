#!/usr/bin/python

import sqlite3
import getopt
import sys

def main():

    con = sqlite3.connect('tareas.db')
    cur = con.cursor()

    # Errores posibles
    # Faltan argumentos necesarios
    # No se dan valores a los argumentos

    try:
        opciones, args = getopt.getopt(sys.argv[1:], None, ["crear-tarea",
            "eliminar-tarea=", "actualizar-tarea=", "descripcion=",
            "mostrar-tareas="])
    except getopt.GetoptError, e:
        if e.opt == 'descripcion':
            print "Error: Falta descripcion."
        elif e.opt == 'mostrar-tareas':
            print "Error: Falta id de la tarea."
        sys.exit(1)

    crear_tarea = False
    eliminar_tarea = False
    actualizar_tarea = False
    mostrar_tareas = False

    descripcion = ''
    tarea_id = None

    for opc, val in opciones:

        if opc == '--crear-tarea':
                crear_tarea = True
        elif opc == '--eliminar-tarea':
            eliminar_tarea = True
            tarea_id = val
        elif opc == '--actualizar-tarea':
            actualizar_tarea = True
            tarea_id = int(val)
        elif opc == '--descripcion':
            descripcion = val
        elif opc == '--mostrar-tareas':
            mostrar_tareas = True
            tarea_id = int(val)
            break
        else:
            man()
            sys.exit(1)

    if crear_tarea:
        if descripcion == '':
            print "Error: Falta descripcion."
            sys.exit(1)
        else:
            cur.execute('INSERT INTO tareas (descripcion, lista_id) VALUES (?, 1)', (descripcion,))

    elif eliminar_tarea:
        cur.execute('DELETE FROM tareas WHERE id=?', (tarea_id,))

    elif actualizar_tarea:
        cur.execute('UPDATE tareas SET descripcion=? WHERE id=?', (descripcion, tarea_id,))

    elif mostrar_tareas:

        if tarea_id == 0:
            cur.execute('SELECT id, descripcion FROM tareas')
        else:
            cur.execute('SELECT id, descripcion FROM tareas WHERE id=?', (tarea_id,))

        tareas = cur.fetchall()
        for tarea in tareas:
            print "%s - %s" % (tarea[0], tarea[1],)

    con.commit()
    con.close()

if __name__ == '__main__':
    main()
    sys.exit(0)
