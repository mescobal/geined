#!/usr/bin/env ruby
require 'cgi_exception'
require 'funciones'
require 'datos'
require 'htm'
def listado
  pag = Pagina.new('Listado de productos', 5)
	boton("Nuevo", "prod.rb?accion=nuevo")
	boton('Volver', 'geined.py?accion=administracion')
	# cargar datos
  productos = Producto.find(:all, :order=>:producto)
	encabezado_tabla(["Nº", "Producto", "Rubro", "Precio", "Acciones"])
  i = 0
	productos.each do |fila|
    fila_alterna(i)
		celda(fila.id)
		celda(fila.producto)
		celda(fila.rubro)
		celda(moneda(fila.precio))
		print '<td>'
		boton("Detalle", "prod_ver.php?cuenta_id=#{fila.id}")
		boton("Editar", "prod.rb?id=#{fila.id}&accion=editar")
		boton("Borrar", "prod.rb?accion=confirmar&id=#{fila.id}")
		puts '</td></tr>'
    i = i + 1
  end
	fin_tabla
	boton("Volver",'geined.py?accion=administracion')
	pag.fin
end
def nuevo
  pag = Pagina.new('Nuevo producto', 4)
  cuentas_combo = Cuenta.find_by_sql('SELECT id,CONCAT(rubro,"-",nombre) as selec FROM cuentas ORDER BY rubro')
  form_edicion('Nuevo producto', 'prod.rb')
  puts pag.cgi.hidden('accion', 'agregar')
	input_texto('Producto:','producto','')
  input_combo()
	puts '<tr><td>Rubro:</td><td><input type="text" name="rubro" value="" onChange="codifica()" /> - <input disabled size="80" value="desconocido" name="lblrubro" /></td></tr>'
	input_numero("Precio:","precio","")
	botones
	fin_formulario
	fin_tabla
	boton('Volver','prod.rb?accion=listado')
end
def agregar(frm)
  begin
    productos = Producto.find(:all, :conditions=>{:producto=>frm['producto']})
    duplicado('prod.rb?accion=listado')
  rescue ActiveRecord::RecordNotFound
    Producto.create(
      :producto => frm['producto'],
      :rubro => frm['rubro'],
      :precio => frm['precio'])
    listado
  end
end
def editar(frm)
	# Entrada
  pag = Pagina.new('Edición de producto', 4)
  cuentas = Cuenta.find(:all, :order=>:rubro)
  producto = Producto.find(frm['id'])
  form_edicion("Editar producto", 'prod.rb')
  puts pag.cgi.hidden('accion', 'actualizar')
  puts pag.cgi.hidden('id', frm['id'])
  input_texto('Producto:', producto.producto)
  input_combo('Rubro:', 'cuenta_id', cuentas, ['id', 'rubro', 'nombre'], frm['cuenta_id'])
	input_numero("Precio:", "precio", frm['precio'])
	botones('prod.rb?accion=listado')
	form_edicion_fin
	pag.fin
end
def actualizar(frm)
  Producto.update(frm['id'],{
    :producto => frm['producto'],
    :cuenta_id => frm['cuenta_id'],
    :precio => frm['precio']
  })
  listado
end
if __FILE__ == $0
  form = CGI.new('html4')
  accion = 'listado'
  if form.has_key?('accion')
    accion = form['accion']
  end
  case accion
  when 'listado'
    listado
  when 'editar'
    editar(form)
  when 'actualizar'
    actualizar(form)
  when 'nuevo'
    nuevo
  when 'agregar'
    agregar(form)
  when 'eliminar'
    Producto.delete(form['id'])
    listado
  end
end