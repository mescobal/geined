#!/usr/bin/env ruby
class File
  def replace(pattern, string)
    full_path = File.expand_path path
    return if !File.file?(full_path)
 
    reopen(full_path, 'r')
    lines = readlines
 
    changes = false
    lines.each do |line|
      changes = true if line.gsub!(pattern, string)
    end
 
    if changes
      reopen(full_path, 'w')
      lines.each do |line|
        write(line)
      end
      close
    end
  end
end

if ARGV.count != 3
    puts "Error: argumentos incorrectos"
    puts "Uso: srchrep.rb cadena_buscar cadena_reemplazar archivos"
    puts "Donde 'archivos' es una lista de archivos en formato *.* entre comillas "
else
    # ver si existe archivo
    # hacer una lista de archivos que tengan la cadena buscada
    files = Dir.glob(ARGV[2])
    numarch = files.count
    # por cada archivo de la lista
    for filename in files
        arch = File.open(filename)
        arch.replace(/#{ARGV[0]}/,ARGV[1])
    end
end
