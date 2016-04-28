def base_message(sender, message):
  return {
    'recipient': {
      'id': sender
    },
    'message': message
  }

def button_template(sender, text, buttons):
  return generic_template(sender, {
    'template_type': 'button',
    'text': text,
    'buttons': buttons
  })

def generic_template(sender, payload):
  return base_message(sender, {
    'attachment': {
      'type': 'template',
      'payload': payload
    }
  })

def button(button_type, title, url, payload = None):
  button_obj = {
    'type': button_type,
    'title': title,
    'url': url
  }

  if button_type == 'postback':
    button_obj['payload'] = payload
  
  return button_obj

