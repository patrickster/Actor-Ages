
FixBirthdate <- function(birthdate) {
  ## If only birth year is known, assume date was June 1st
  if (nchar(birthdate) == 4) {
    birthdate <- paste(birthdate, "06-01", sep="-")
  }
  return(birthdate)
}


FormatChart <- function(chart) {
  
  ## Clarify column names
  names(chart)[names(chart) == "id"] <- "film.id"
  names(chart)[names(chart) == "date"] <- "release.date"
  
  ## Convert grosses to numeric
  chart$gross <- sapply(chart$gross, function(x) gsub("[^0-9]", "", x))
  chart$gross <- as.numeric(chart$gross)

  ## Convert release data to Date format
  chart$release.date <- as.Date(chart$release.date)

  return(chart)
}


PrepCast <- function(year, actor.info, max.rank=5, data.dir="data/") {

  ## Load data
  chart <- read.csv(paste(data.dir, "chart-", year, "-resolved.csv", sep=""),
                    as.is=TRUE)
  cast <- read.csv(paste(data.dir, "cast-", year, ".csv", sep=""), as.is=TRUE)

  chart <- FormatChart(chart)
  
  ## Merge cast with actor info
  cast <- merge(cast, actor.info[,c("actor.id", "birthdate", "gender")],
                by="actor.id", all.x=TRUE, all.y=FALSE)

  ## Merge cast with chart info
  cols.to.add <- c("film.id", "film", "release.date", "gross", "year")
  cast <- merge(cast, chart[,cols.to.add],
                by="film.id", all.x=TRUE, all.y=FALSE)

  ## Sort
  cast <- cast[order(cast$release.date, cast$film.id, cast$rank),]
  
  return(cast)
}

  
PrepYearlyChart <- function(year, actor.info, max.rank=5, data.dir="data/") {

  ## Load data
  chart <- read.csv(paste(data.dir, "chart-", year, "-resolved.csv", sep=""),
                    as.is=TRUE)
  cast <- read.csv(paste(data.dir, "cast-", year, ".csv", sep=""), as.is=TRUE)

  ## Merge cast with actor info
  cast <- merge(cast, actor.info[,c("actor.id", "birthdate", "gender")],
                by="actor.id", all.x=TRUE, all.y=FALSE)
  
  chart <- FormatChart(chart)
  
  ## Find top-billed actor and actress in each cast
  cast <- cast[cast$rank <= max.rank,]
  cast <- cast[order(cast$film.id, cast$rank),]
  
  actresses <- cast[which(cast$gender == "female"),]
  actors <- cast[which(cast$gender == "male"),]
  
  top.actresses <- actresses[-which(duplicated(actresses$film.id)),]
  top.actresses <- top.actresses[,c("film.id", "actor", "birthdate")]
  names(top.actresses)[2:3] <- c("actress", "actress.birthdate")
  
  top.actors <- actors[-which(duplicated(actors$film.id)),]
  top.actors <- top.actors[,c("film.id", "actor", "birthdate")]
  names(top.actors)[3] <- "actor.birthdate"

  ## Merge top-billed actors and actresses into chart
  chart <- merge(chart, top.actresses, by="film.id", all.x=TRUE, all.y=FALSE)
  chart <- merge(chart, top.actors, by="film.id", all.x=TRUE, all.y=FALSE)

  ## Sort by gross
  chart <- chart[order(chart$gross, decreasing=TRUE),]
  chart$year.rank <- 1:nrow(chart)

  ## Convert date fields to Date format
  chart$actress.birthdate <- as.Date(chart$actress.birthdate)
  chart$actor.birthdate <- as.Date(chart$actor.birthdate)

  ## Calculate actor/actress ages
  chart$actress.age <- (chart$release.date - chart$actress.birthdate) / 365
  chart$actress.age <- as.numeric(chart$actress.age)
  chart$actor.age <- (chart$date - chart$actor.birthdate) / 365
  chart$actor.age <- as.numeric(chart$actor.age)
  
  return(chart)
}



data.dir <- "data/"
min.year <- 1999
max.year <- 2012

## Load actor info file
actor.info <- read.csv(paste(data.dir, "actor-info.csv", sep=""), as.is=TRUE)
actor.info$birthdate <- sapply(actor.info$birthdate, FixBirthdate)

## Create/concatenate datasets for specified years
chart <- casts <- c() 
for (year in min.year:max.year) {
  chart.tmp <- PrepYearlyChart(year, actor.info, max.rank=5)
  chart <- rbind(chart, chart.tmp)
  casts.tmp <- PrepCast(year, actor.info, max.rank=5)
  casts <- rbind(casts, casts.tmp)
}

## Save prepped datasets
rm(ls=setdiff(ls(), c("chart", "casts")))
save.image("data.Rdata")
