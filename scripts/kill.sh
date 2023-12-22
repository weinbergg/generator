# Поиск PID процессов, использующих порт 5000
pid_list=$(lsof -t -i :5000)

if [ -z "$pid_list" ]; then
  echo "Нет процессов, использующих порт 5000"
else
  # Перебор и завершение процессов по PID
  for pid in $pid_list; do
    echo "Завершение процесса с PID $pid"
    kill $pid
  done
fi