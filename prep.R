
FixBirthdate <- function(birthdate) {
  ## If only birth year is known, assume date was June 1st
  if (nchar(birthdate) == 4) {
    birthdate <- paste(birthdate, "06-01", sep="-")
  }
  return(birthdate)
}


PrepYearlyChart <- function(year, actor.info, max.rank=5) {

  ## Load data
  chart <- read.csv(paste(data.dir, "chart-", year, "-resolved.csv", sep=""),
                    as.is=TRUE)
  cast <- read.csv(paste(data.dir, "cast-", year, ".csv", sep=""), as.is=TRUE)

  ## Merge cast with actor info
  cast <- merge(cast, actor.info[,c("actor.id", "birthdate", "gender")],
                by="actor.id", all.x=TRUE, all.y=FALSE)

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
  names(chart)[6] <- "film.id"
  chart <- merge(chart, top.actresses, by="film.id", all.x=TRUE, all.y=FALSE)
  chart <- merge(chart, top.actors, by="film.id", all.x=TRUE, all.y=FALSE)

  ## Convert grosses to numeric
  chart$gross <- sapply(chart$gross, function(x) gsub("[^0-9]", "", x))
  chart$gross <- as.numeric(chart$gross)

  ## Sort by gross
  chart <- chart[order(chart$gross, decreasing=TRUE),]
  chart$year.rank <- 1:nrow(chart)

  ## Convert date fields to Date format
  chart$date <- as.Date(chart$date)
  chart$actress.birthdate <- as.Date(chart$actress.birthdate)
  chart$actor.birthdate <- as.Date(chart$actor.birthdate)

  ## Calculate actor/actress ages
  chart$actress.age <- as.numeric((chart$date - chart$actress.birthdate) / 365)
  chart$actor.age <- as.numeric((chart$date - chart$actor.birthdate) / 365)

  return(chart)
}



data.dir <- "data/"
min.year <- 1999
max.year <- 2012

## Load actor info file
actor.info <- read.csv(paste(data.dir, "actor-info.csv", sep=""), as.is=TRUE)
actor.info$birthdate <- sapply(actor.info$birthdate, FixBirthdate)

## Create/concatenate charts for specified years
chart <- c()
for (year in min.year:max.year) {
  chart.tmp <- PrepYearlyChart(year, actor.info, max.rank=5)
  chart <- rbind(chart, chart.tmp)
}

