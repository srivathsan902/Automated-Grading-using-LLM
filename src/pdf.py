from fpdf import FPDF
import os


title = 'Performance Report'
class PDF(FPDF):
    def header(self):
        self.image('assets/logo.jpg', 10, 8, 25)
        image_w = 25
        self.set_font('helvetica', 'B', 20)
        title_w = self.get_string_width(title) + 6
        
        doc_width = self.w
        self.set_x((doc_width - title_w) / 2)

        self.set_draw_color(0, 0, 0)
        self.set_fill_color(255,255,255)
        self.set_text_color(0,0,0)

        self.set_line_width(1)

        self.cell(title_w, 10, title, border = 1, ln= 1, align = 'C', fill = 1)

        self.ln(20)

    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', 'I', 8)
        self.set_text_color(169, 169, 169)
        self.cell(0, 10, f'Page {self.page_no()}/{{nb}}', 0, 0, 'C')
        
