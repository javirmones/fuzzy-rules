import itertools
import re
from tkinter import X
from reportlab.lib import pagesizes
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, inch
from random import randint
from statistics import mean

from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.platypus.flowables import PageBreak

def readable_rules(rules):
    string_list = []
    for x in range(0, len(rules)):
        flag = False
        regla = rules[x]

        string = str(regla[0])+": if"
        count = 0
        
        for y in range(0, len(regla[1])):
            tag = regla[1][y]
            
            if tag != 0:
                if flag == False:
                    flag = True
                else:
                    string += " and"
                count += 1
                if count == 2 :
                    string += " X"+str(y) +" is " + str(tag) + '\n'
                else:
                    string += " X"+str(y) +" is " + str(tag)

        final_string = string + " then " +str(regla[3]) + " created with: "+str(regla[2])+ " examples."
        string_list.append(final_string)
    return string_list 

def grouper(iterable, n):
    args = [iter(iterable)] * n
    return itertools.zip_longest(*args)

def create_text(tiempo, avg_amp, average_mean, dict_rules_amp, class_names, ej_list, algorithm, division, len_total_amp, n_vars, examples_len, tuple_list_amp_f, author):
    w, h = A4
    x_offset = 50
    max_rows_per_page = 45
    y_offset = 50
    # Space between rows.
    padding = 15
    xlist = [x + x_offset for x in [0, 50, 110, 170, 230, 280, 350, 400, 480 ]]
    ylist = [h - 200 - y_offset - i*padding for i in range(max_rows_per_page + 1)]

    
    data = [["Prueba"] + class_names + ["Total", "Acierto", "NC", "Fallo"]]

    for i in range(0,len(ej_list)):
        elemento_len = len_total_amp[i]
        avg = avg_amp[i]
        data.append([f"{i+1}", elemento_len[0], elemento_len[1], elemento_len[2], sum(elemento_len), str(avg[0])+"%", str(avg[1])+"%", str(avg[2])+"%"])

 
    text = ""
    
    for x in range(0, len(ej_list)):
        #text_it = c.beginText(50, h - 50)
        #text_it.setFont("Courier-Bold",10)
        #text_it.textLine("--Algoritmo "+algorithm+" Iteracion "+str(x+1)+"--")
        text += "<b>--Algoritmo "+algorithm+" Iteracion "+str(x+1)+"-- </b><br/><br/>"
        #text_it.setFont("Courier",8)
        dict_item = dict_rules_amp[x]
        avg = avg_amp[x]
        keys_dict = list(dict_item.keys())
        values_dict = list(dict_item.values())
        new_list = []
        for y in range(0, len(values_dict)):
     
            new_list.append([keys_dict[y], values_dict[y][0], values_dict[y][1], values_dict[y][2]])

        rules_of_classes = []
        def_rules = []
        for x in range(0, len(class_names)):
            class_rul = []
            for z in range(0, len(new_list)):
                el = new_list[z]
                if el[3] == class_names[x]:
                    class_rul.append(el)
            rules_of_classes.append(class_rul)


        for y in rules_of_classes:
            def_rules.append(readable_rules(y))

        #text_it.setFont("Courier-Bold",8)
        #text_it.textLine("Reglas Iris setosa: " +str(len(iris_setosa)))
        #text_it.setFont("Courier",8)
        for x in range(0, len(class_names)):
            rules = def_rules[x]
            text += "<br/>"
            text += "<b> Reglas "+ class_names[x] +" : " +str(len(rules)) +"</b> <br/><br/>"
            for a in rules:
                text += a +"<br/>"
            text += "<br/>"
        #text_it.textLine("")
        #text_it.setFont("Courier-Bold",8)
        #text_it.textLine("Reglas Iris versicolor: " +str(len(iris_versicolor)))
        
        text += "<br/>"
        text += "<br/>"
        #text_it.textLine("Pruebas realizadas con: " +str(len(data_tests))+" ejemplos")
        cpr = 0
        for y in range(0, len(tuple_list_amp_f[x])):
            cpr +=1
            element = tuple_list_amp_f[x][y]
            if cpr == 1:
                
                text += "<b>" + str(element) + "</b> <br/>"
                #text_it.setFont("Courier-Bold",8)
                #text_it.textLine(str(element))
            else:
                if element[6] == "Acierto":
                    text += '<font name="Courier" size="10" color="green">'+str(element)+ '</font> <br/>'
                elif element[6] == "No clasificado":
                    text += '<font name="Courier" size="10" color="orange">'+str(element)+ '</font> <br/>'
                elif element[6] == "Fallo":
                    text += '<font name="Courier" size="10" color="red">'+str(element)+ '</font> <br/>'
                #text_it.setFont("Courier",8)
                #text_it.textLine(str(element))
        text += "<br/>"
        text += "<br/>"
        #text_it.textLine("")
        #text_it.setFont("Courier-Bold",8)
        text += '<font name="Courier" size="10" color="green"> P. Acierto: '+str(avg[0])+ '%' + '</font> <br/>'
        text += '<font name="Courier" size="10" color="orange"> P. No Clasificados: '+ str(avg[1])+ '%' + '</font> <br/>'
        text += '<font name="Courier" size="10" color="red"> P. Fallo: '+ str(avg[2])+ '%' + '</font> <br/> <br/>'
  
        #text_it.textLine("P. de acierto "+str(avg[0]) +"%"+ "  P. No clasificados: "+str(avg[1])+"% "+"  P. Fallo: "+str(avg[2])+"%")
        #c.drawText(text_it)
        #c.showPage()
    text += "<b>--- Informe de resultados del algoritmo --- </b>" +algorithm + "<br/>"
    text += "Numero total de ejemplos: " +str(examples_len[0]) + "<br/>"
    text += "Numero de clases: "+ str(len(class_names)) + "<br/>"
    text += "Numero de variables: "+ str(n_vars) + "<br/>"
    text += "Porcentaje de ejemplos usados para entrenamiento: " +str(division[0]) +"%" + "<br/>"
    text += "Porcentaje de ejemplos usados para test: " +str(division[1]) +"%" + "<br/>"
    text += "Numero total de ejemplos entrenamiento: " +str(examples_len[1]) + "<br/>"
    text += "Numero total de ejemplos test: " +str(examples_len[2]) + "<br/>"
    text += "Numero total de ejecuciones: " +str(len(ej_list)) + "<br/>"
    text += "Tiempo de ejecucion del algoritmo: " +str(tiempo) +"s" + "<br/> <br/>"
    text += "<b>----Resumen pruebas algoritmo----</b>" + "<br/>"
    text += author + "<br/>"
    text += '<font name="Courier" size="10" color="green"> Media de P. Acierto: '+ str(average_mean[0])+ '%' + '</font> <br/>'
    text += '<font name="Courier" size="10" color="orange"> Media de P. No Clasificados: '+ str(average_mean[1])+ '%' + '</font> <br/>'
    text += '<font name="Courier" size="10" color="red"> Media de P. No Clasificados: '+ str(average_mean[2])+ '%' + '</font> <br/> <br/>'
 

    return text, data

def build_pdf(text_amp, data_amp, text_else, data_else, final_list, legend, path):

    pdf = SimpleDocTemplate(path, pagesize=A4)
    flow_object = []
    styles = ParagraphStyle(
        name='Normal',
        fontName='Courier',
        fontSize=10,
    )
    table_amp = Table(data_amp, 8*[0.9*inch], len(data_amp)*[0.4*inch])
    table_amp.setStyle(TableStyle([
    ('TEXTCOLOR',(5,0),(5, len(data_amp)),colors.green),
    ('FONTNAME',(0, 0), (7, 0), 'Courier-Bold' ),
    ('FONTNAME', (0,1), (7, len(data_amp)), 'Courier'),
    ('TEXTCOLOR',(6, 0),(6, len(data_amp)),colors.orange),
    ('TEXTCOLOR',(7, 0),(7, len(data_amp)),colors.red),
    ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
    ('BOX', (0,0), (-1,-1), 0.25, colors.black),
    ]))
    table_else = Table(data_else, 8*[0.9*inch], len(data_amp)*[0.4*inch])
    table_else.setStyle(TableStyle([
    ('TEXTCOLOR',(5,0),(5, len(data_amp)),colors.green),
    ('FONTNAME',(0, 0), (7, 0), 'Courier-Bold' ),
    ('FONTNAME', (0,1), (7, len(data_amp)), 'Courier'),
    ('TEXTCOLOR',(6, 0),(6, len(data_amp)),colors.orange),
    ('TEXTCOLOR',(7, 0),(7, len(data_amp)),colors.red),
    ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
    ('BOX', (0,0), (-1,-1), 0.25, colors.black),
    ]))



    header = [["Amplify algorithm" , "Elsevier algorithm"]]
    header_table = Table(header, 2*[3.75*inch], 1*[0.4*inch])
    header_table.setStyle(TableStyle([
    ('FONTNAME',(0, 0), (2, 0), 'Courier-Bold' ),
    ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
    ('BOX', (0,0), (-1,-1), 0.25, colors.black),
    ]))

    table_final = Table(final_list, 15*[0.5*inch], len(final_list)*[0.4*inch])
    table_final.setStyle(TableStyle([
    ('TEXTCOLOR',(5,0),(5, len(final_list)),colors.green),
    ('FONTNAME',(0, 0), (15, 0), 'Courier-Bold' ),
    ('FONTNAME', (0,1), (15, len(final_list)), 'Courier'),
    ('TEXTCOLOR',(6, 0),(6, len(final_list)),colors.orange),
    ('TEXTCOLOR',(7, 0),(7, len(final_list)),colors.red),
    ('TEXTCOLOR',(12,0),(12, len(final_list)),colors.green),
    ('TEXTCOLOR',(13, 0),(13, len(final_list)),colors.orange),
    ('TEXTCOLOR', (14, 0),(14, len(final_list)),colors.red),
    ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
    ('BOX', (0,0), (-1,-1), 0.25, colors.black),
    ]))

    p_text = Paragraph(text_amp, style=styles)
    flow_object.append(p_text)
    flow_object.append(table_amp)
    flow_object.append(PageBreak())
    else_p = Paragraph(text_else, style=styles)
    flow_object.append(else_p)
    flow_object.append(table_else)
    flow_object.append(PageBreak())
    flow_object.append(header_table)
    flow_object.append(table_final)
    header_legend = Paragraph(legend, style=styles)
    flow_object.append(header_legend)
    pdf.build(flow_object)


def build_amp_pdf(text_amp, data_amp, path):

    pdf = SimpleDocTemplate(path, pagesize=A4)
    flow_object = []
    styles = ParagraphStyle(
        name='Normal',
        fontName='Courier',
        fontSize=10,
    )
    table_amp = Table(data_amp, 8*[0.9*inch], len(data_amp)*[0.4*inch])
    table_amp.setStyle(TableStyle([
    ('TEXTCOLOR',(5,0),(5, len(data_amp)),colors.green),
    ('FONTNAME',(0, 0), (7, 0), 'Courier-Bold' ),
    ('FONTNAME', (0,1), (7, len(data_amp)), 'Courier'),
    ('TEXTCOLOR',(6, 0),(6, len(data_amp)),colors.orange),
    ('TEXTCOLOR',(7, 0),(7, len(data_amp)),colors.red),
    ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
    ('BOX', (0,0), (-1,-1), 0.25, colors.black),
    ]))
    p_text = Paragraph(text_amp, style=styles)
    flow_object.append(p_text)
    flow_object.append(table_amp)
    flow_object.append(PageBreak())
    pdf.build(flow_object)

def build_els_pdf(text_else, data_else, path):

    pdf = SimpleDocTemplate(path, pagesize=A4)
    flow_object = []
    styles = ParagraphStyle(
        name='Normal',
        fontName='Courier',
        fontSize=10,
    )

    table_else = Table(data_else, 8*[0.9*inch], len(data_else)*[0.4*inch])
    table_else.setStyle(TableStyle([
    ('TEXTCOLOR',(5,0),(5, len(data_else)),colors.green),
    ('FONTNAME',(0, 0), (7, 0), 'Courier-Bold' ),
    ('FONTNAME', (0,1), (7, len(data_else)), 'Courier'),
    ('TEXTCOLOR',(6, 0),(6, len(data_else)),colors.orange),
    ('TEXTCOLOR',(7, 0),(7, len(data_else)),colors.red),
    ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
    ('BOX', (0,0), (-1,-1), 0.25, colors.black),
    ]))

 
    else_p = Paragraph(text_else, style=styles)
    flow_object.append(else_p)
    flow_object.append(table_else)
    pdf.build(flow_object)
