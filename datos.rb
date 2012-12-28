#!/usr/bin/env ruby
require 'rubygems'
require 'active_record'
#require 'column_patch'
#ActiveSupport::CoreExtensions::Time::Conversions::DATE_FORMATS.merge!(:default => '%d/%m/%Y %H:%M')
# ActiveSupport::CoreExtensions::Date::Conversions::DATE_FORMATS.merge!(:default => '%d/%m/%Y')
# ActiveSupport::CoreExtensions::Time::Conversions::DATE_FORMATS.merge!(:default => '%d/%m/%Y %H:%M')
# ActiveRecord::ConnectionAdapters::Quoting.send(:include, QuotingPatch)
# ActiveRecord::ConnectionAdapters::Column.string_to_date(string)


ActiveRecord::Base.establish_connection(
    :adapter => 'mysql',
    :host => 'localhost',
    :user => 'mescobal',
    :password => 'pacu2000',
    :database  => 'Alianza'
)
class Alumno < ActiveRecord::Base
  set_table_name 'alumnos'
  belongs_to :cliente
end
class Balcom < ActiveRecord::Base
    set_table_name 'balcom'
end
class Bie_cam < ActiveRecord::Base
    set_table_name 'bie_cam'
    has_many :existencias
end
class Cat_cliente < ActiveRecord::Base
    set_table_name 'cat_clientes'
    belongs_to :cliente
end
class Cat_empleado < ActiveRecord::Base
    has_many :empleados
end
class Cliente < ActiveRecord::Base
  has_many :alumnos
  has_many :cta_clientes
end
class Conciliacion < ActiveRecord::Base
    set_table_name 'conciliacion'
end
class Cta_cliente < ActiveRecord::Base
    belongs_to :cliente
end
class Cta_empleado < ActiveRecord::Base
    set_table_name 'cta_empleados'
    belongs_to :empleado
end
class Cuenta < ActiveRecord::Base
  has_many :transacciones
end
class Curso < ActiveRecord::Base
    belongs_to :tipo_curso
end
class Deposito < ActiveRecord::Base
    has_many :existencias
end
class Empleado < ActiveRecord::Base
    belongs_to :cat_empleados
end
class Existencia < ActiveRecord::Base
    belongs_to :deposito
    belongs_to :bie_cam
end
class Inventario < ActiveRecord::Base
    set_table_name 'inventario'
end
class Llamada < ActiveRecord::Base
    set_table_name 'llamadas'
    belongs_to  :clientes
end
class Producto < ActiveRecord::Base
  set_table_name 'productos'
end
class Tipo_curso < ActiveRecord::Base
    set_table_name 'tipo_curso'
    has_many :cursos
end
class Tipo_pago < ActiveRecord::Base
    set_table_name 'tipo_pago'
    has_many    :alumnos
end
class Transaccion < ActiveRecord::Base
  set_table_name 'transacciones'
  belongs_to :cuenta
end
class Usuario < ActiveRecord::Base
    set_primary_key 'usuario'
end
