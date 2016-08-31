struct Question {
  1: i32 id,
  2: string user,
  3: string question
}

service  Publish{
  void save(1: Question Qt)
}
