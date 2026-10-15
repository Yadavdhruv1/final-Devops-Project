# ─── AWS Provider Configuration ───

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Project     = "finpilot"
      Environment = var.environment
      ManagedBy   = "terraform"
    }
  }
}
