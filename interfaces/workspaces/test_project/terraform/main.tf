# Test terraform file
resource "aws_instance" "test" {
  ami = "ami-12345678"
  instance_type = "t2.micro"
}