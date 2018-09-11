library('geojsonio')


path_of_file<-'apd_beat.geojson'
beats_geo=geojsonio::geojson_read(path_of_file,what='sp')
n.beats<-length(beats_geo)

station_locations<-read.csv('total_data_of_georgia.csv')

data_matrix_2=matrix(nrow=80,ncol=30)

for(i in 1:80){
  data_matrix_2[i,1]=as.character(beats_geo@data[["BEAT"]][i])
  j<-2
  for(num in 1:25813){
      if(point.in.polygon(station_locations[num,3],station_locations[num,2],c(beats_geo@polygons[[i]]@Polygons[[1]]@coords[,1]),c(beats_geo@polygons[[i]]@Polygons[[1]]@coords[,2]))==1){
        data_matrix_2[i,j]<-as.character(station_locations[num,1])
        #print(as.character(station_locations[num,1]))
        j<-j+1}
  }

}
print(data_matrix_2[80,])

