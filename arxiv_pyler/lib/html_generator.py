from htmltag import html, head, body, title, div, ol, li, a, p

#input:
#    entry_list: a list whose items are dicts returned by arxiv_repsonse_parser
#output:
#    the html
def html_generator(entry_list):
    print 'generating html'
    f = open('output.html', 'w')

    #html5
    f.write('<!DOCTYPE html>')
    f.write('<html>')

    #head
    #meta_string = '<meta charset="utf-8" name="viewport" content="width=device-width, initial-scale=1.0">'
    title_string = title('arXiv:PDF')
    #head_string = head(''.join([meta_string, title_string]))
    head_string = head(title_string)
    f.write(head_string)

    #body
    f.write('<body>')
    for entry in entry_list:
      file_link = a(entry['title'], href=entry['file_source'])
      entry_title_string = p(file_link)
      id_string = p(entry['identifier'])
      author_string = p(', '.join(entry['author']))
      summary_string = p(entry['summary'])

      entry_string = ''.join([
        entry_title_string, 
        id_string, 
        author_string, 
        summary_string
      ])
      f.write(entry_string)
    f.write('</body>')

    f.write('<html>')
    
    f.close()