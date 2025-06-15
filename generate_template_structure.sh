#!/bin/bash

# Set base directory for templates
TEMPLATES_DIR="templates/project"
PACKAGE_PATH="{{ base_package_path }}"  # Jinja placeholder

# Define directories to create
DIRS=(
  "$TEMPLATES_DIR/config"
  "$TEMPLATES_DIR/logs"
  "$TEMPLATES_DIR/src/main/java/$PACKAGE_PATH/controller"
  "$TEMPLATES_DIR/src/main/java/$PACKAGE_PATH/dto"
  "$TEMPLATES_DIR/src/main/java/$PACKAGE_PATH/entity"
  "$TEMPLATES_DIR/src/main/java/$PACKAGE_PATH/service/impl"
  "$TEMPLATES_DIR/src/main/java/$PACKAGE_PATH/mapper"
  "$TEMPLATES_DIR/src/main/java/$PACKAGE_PATH/config"
  "$TEMPLATES_DIR/src/main/java/$PACKAGE_PATH/aspect"
  "$TEMPLATES_DIR/src/main/java/$PACKAGE_PATH/common/audit"
  "$TEMPLATES_DIR/src/main/java/$PACKAGE_PATH/common/constants"
  "$TEMPLATES_DIR/src/main/java/$PACKAGE_PATH/common/enums"
  "$TEMPLATES_DIR/src/main/java/$PACKAGE_PATH/common/exception"
  "$TEMPLATES_DIR/src/main/java/$PACKAGE_PATH/common/helper"
  "$TEMPLATES_DIR/src/main/java/$PACKAGE_PATH/common/response"
  "$TEMPLATES_DIR/src/main/java/$PACKAGE_PATH/common/utils"
  "$TEMPLATES_DIR/src/main/java/$PACKAGE_PATH/filter"
  "$TEMPLATES_DIR/src/main/java/$PACKAGE_PATH/helper"
  "$TEMPLATES_DIR/src/main/java/$PACKAGE_PATH/repository"
  "$TEMPLATES_DIR/src/main/java/$PACKAGE_PATH/security"
  "$TEMPLATES_DIR/src/main/java/$PACKAGE_PATH/util"
  "$TEMPLATES_DIR/src/main/resources/db/migration"
  "$TEMPLATES_DIR/src/test/java/$PACKAGE_PATH"
  "$TEMPLATES_DIR/src/test/resource"
)

# Create all directories
for dir in "${DIRS[@]}"; do
  mkdir -p "$dir"
done

# Create template files with .j2 extension
touch "$TEMPLATES_DIR/pom.xml.j2"
touch "$TEMPLATES_DIR/mvnw.j2"
touch "$TEMPLATES_DIR/mvnw.cmd.j2"

touch "$TEMPLATES_DIR/config/application.yml.j2"
touch "$TEMPLATES_DIR/config/application-dev.yml.j2"
touch "$TEMPLATES_DIR/config/application-prod.yml.j2"
touch "$TEMPLATES_DIR/config/application-test.yml.j2"

touch "$TEMPLATES_DIR/logs"

touch "$TEMPLATES_DIR/src/main/java/$PACKAGE_PATH/MdmBackendApplication.java.j2"
touch "$TEMPLATES_DIR/src/main/java/$PACKAGE_PATH/controller/BaseController.java.j2"
touch "$TEMPLATES_DIR/src/main/java/$PACKAGE_PATH/dto/BaseDTO.java.j2"
touch "$TEMPLATES_DIR/src/main/java/$PACKAGE_PATH/entity/BaseEntity.java.j2"
touch "$TEMPLATES_DIR/src/main/java/$PACKAGE_PATH/service/BaseService.java.j2"
touch "$TEMPLATES_DIR/src/main/java/$PACKAGE_PATH/service/impl/BaseServiceImpl.java.j2"
touch "$TEMPLATES_DIR/src/main/java/$PACKAGE_PATH/mapper/BaseMapper.java.j2"
touch "$TEMPLATES_DIR/src/main/resources/banner.txt.j2"
touch "$TEMPLATES_DIR/src/main/resources/logback-spring.xml.j2"
touch "$TEMPLATES_DIR/src/main/resources/db/migration/V1__init_schema.sql.j2"

echo "✅ Template directory structure created at: $TEMPLATES_DIR"
