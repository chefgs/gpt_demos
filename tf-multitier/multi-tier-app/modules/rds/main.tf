resource "aws_db_subnet_group" "db_subnet_group" {
  name       = "db-subnet-group"
  subnet_ids = var.subnet_ids

  tags = {
    Name = "db-subnet-group"
  }
}

resource "aws_db_instance" "db" {
  identifier              = var.db_identifier
  allocated_storage       = var.allocated_storage
  engine                  = var.engine
  engine_version          = var.engine_version
  instance_class          = var.instance_class
  name                    = var.db_name
  username                = var.username
  password                = var.password
  db_subnet_group_name    = aws_db_subnet_group.db_subnet_group.name
  vpc_security_group_ids  = var.security_group_ids
  skip_final_snapshot     = true

  tags = {
    Name = var.db_identifier
  }
}
