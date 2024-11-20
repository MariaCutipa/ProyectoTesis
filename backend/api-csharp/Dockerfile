FROM mcr.microsoft.com/dotnet/sdk:8.0 AS create
WORKDIR /src
RUN dotnet new webapi -o api-csharp --no-https
COPY ./Program.cs ./api-csharp/Program.cs


FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /src
COPY --from=create /src/api-csharp/api-csharp.csproj .
RUN dotnet restore
COPY --from=create /src/api-csharp .
RUN dotnet publish -c release -o /app


FROM mcr.microsoft.com/dotnet/aspnet:8.0
WORKDIR /app
COPY --from=build /app .
EXPOSE 8080
ENTRYPOINT ["dotnet", "api-csharp.dll"]