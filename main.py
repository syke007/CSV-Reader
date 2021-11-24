import ply.lex as plex

class virgulas:
    tokens = ("COMMENTS", "QUANTATION", "COMMA")
    t_ignore = " "

    def t_COMMENTS(self, t):
        r"\#[^\n]+"           ##para #
        pass

    def t_QUANTATION(self, t):
        r"(,?)\"[^\"]+(\"?),?"    ## para as "
        return t

    def t_COMMA(self, t):      ## ler até ás virgulas
        r"(,?)[^\,]+,?"
        return t

    def t_error(self, t):
        print(f"Unexpected tokens: {t.value[:10]}")
        exit(1)

    def __init__(self, filename):
        self.lexer = None
        self.filename = filename
        self.inside_header = False
        self.html = []
        self.latex = []

    def toc(self, **kwargs):
        i = 0
        header = True
        self.lexer = plex.lex(module=self, **kwargs)

        with open(self.filename, "r") as fh:
            contents = fh.readlines()
        ab = []
        h = []
        for item in contents:
            self.lexer.input(item)

            temphtml = []
            tempLatex = []
            x = 0

            for token in iter(self.lexer.token, None):
                if token.value != "\n":
                    token.value = token.value.replace("\n", "")
                    token.value = token.value.replace("\"", "")
                    token.value = token.value.replace(",", "")
                    if header == True:
                        h.append("("+str(i+1)+") -> "+token.value+" | ")
                        temphtml.append("<th>"+str(token.value)+"</th>")
                        #Col1 & Col2 & Col2 & Col3 & Col3
                        tempLatex.append(str(token.value)+" & ")
                        i = i + 1
                    else:
                        temphtml.append("<td>" + str(token.value) + "</td>")
                        tempLatex.append(str(token.value)+" & ")

            if header == True:
                str0 = ""
                str0 = str0.join(h)
                choice = input( str0+" -> ")
                ab = choice.split()
                temphtml2 = []
                tempLatex2 = []

                for z in ab:
                    temphtml2.append(temphtml[int(z)-1])
                    tempLatex2.append(tempLatex[int(z)-1])

                tempLatex = []
                temphtml = []

                temphtml = temphtml2

                tempLatex = tempLatex2

                str1 = " "
                str1 = str1.join(temphtml)
                self.html.append("<tr>")
                self.html.append(str1)
                self.html.append("</tr>")

                c = "c"
                for a in range(0, len(tempLatex) - 1):
                    c = c + " c"

                self.latex.append("\\begin{tabular}{||" + c + "||}  \hline")
                tempLatex[len(tempLatex) - 1] = tempLatex[len(tempLatex) - 1][:-2] + " \\\ [0.5ex] "

                str2 = " "
                str2 = str2.join(tempLatex)
                self.latex.append(str2)
                self.latex.append(" \hline")

            if temphtml and header == False:

                temphtml3 = []

                for x in ab:
                    temphtml3.append(temphtml[int(x)-1])

                temphtml = []

                temphtml = temphtml3

                str1 = " "
                str1 = str1.join(temphtml)
                self.html.append("<tr>")
                self.html.append(str1)
                self.html.append("</tr>")


                if tempLatex:
                    tempLatex3  = []

                    for x in ab:
                        tempLatex3.append(tempLatex[int(x)-1])

                    tempLatex = []
                    tempLatex = tempLatex3


                    tempLatex[len(tempLatex) - 1] = tempLatex[len(tempLatex)-1][:-2]+" \\\ "
                    str3 = " "
                    str3 = str3.join(tempLatex)

                    self.latex.append(str3)
                    self.latex.append(" \hline")


            header = False
        return [self.html, self.latex]
        print("Finished processing")

    def escreverHtml(self, table):
        str1 = " "
        str1 = str1.join(table)
        text = '''<html>
        <head>
        <style>
        table {
          font-family: arial, sans-serif;
          border-collapse: collapse;
          width: 100%;
        }

        td, th {
          border: 1px solid #dddddd;
          text-align: left;
          padding: 8px;
        }

        tr:nth-child(even) {
          background-color: #dddddd;
        }
        </style>
        </head>
        <body>
        <table>
        '''+str1

        file = open("tabela.html", "w")
        file.write(text)
        file.close()

    def escreverLatex(self, table):
        str4 = " "
        str4 = str4.join(table)
        text = '''
        \documentclass{article}
            \\begin{document}
            \\begin{center}'''+str4+''''\end{tabular}
            \end{center}
        \end{document} 
        '''

        file = open("tabela.tex", "w")
        file.write(text)
        file.close()


processor = virgulas("teste.csv")
a = processor.toc()
processor.escreverHtml(a[0])
processor.escreverLatex(a[1])
